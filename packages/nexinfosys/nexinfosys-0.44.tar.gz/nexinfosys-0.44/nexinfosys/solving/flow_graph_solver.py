"""
A solver based on the elaboration of a flow graph to quantify interfaces, connected by flow or scale relationships.
It is assumed that other kinds of relationship (part-of, upscale, ...) are translated into these two basic ones.
Another type of relationship considered is linear transform from InterfaceType to InterfaceType, which is cascaded into
appearances of its instances.

Before the elaboration of flow graphs, several preparatory steps:
* Find the separate contexts. Each context is formed by the "local", "environment" and "external" sets of processors,
  and is -totally- isolated from other contexts
  - Context defining attributes are defined in the Problem Statement command. If not, defined, a "context" attribute in
    Processors would be assumed
    If nothing is found, all Processors are assumed to be under the same context (what will happen??!!)
  - Elaborate (add necessary entities) the "environment", "external" top level processors if none have been specified.
    - Opposite processor can be specified when defining Interface
      - This attribute is taken into account if NO relationship originates or ends in this Interface. Then, a default
        relationship would be created
      - If Processors are defined for environment or
* Unexecuted model parts
  - Connection of Interfaces
  - Dataset expansion
* [Datasets]
* Scenarios
  - Parameters
* Time. Classify QQs by time, on storage
* Observers (different versions). Take average always

"""
import traceback
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from typing import Dict, List, Set, Any, Tuple, Union, Optional, NamedTuple, Generator, NoReturn, Sequence

import lxml
import networkx as nx
import pandas as pd
from lxml import etree

from nexinfosys import case_sensitive
from nexinfosys.command_field_definitions import orientations
from nexinfosys.command_generators import Issue, global_functions_extended
from nexinfosys.command_generators.parser_ast_evaluators import ast_evaluator, obtain_subset_of_processors, \
    get_adapted_case_dataframe_filter
from nexinfosys.command_generators.parser_field_parsers import string_to_ast, expression_with_parameters, is_year, \
    is_month, indicator_expression, parse_string_as_simple_ident_list, number_interval
from nexinfosys.common.constants import SubsystemType, Scope
from nexinfosys.common.helper import create_dictionary, PartialRetrievalDictionary, ifnull, istr, strcmp, \
    FloatExp, precedes_in_list, replace_string_from_dictionary, brackets, get_interfaces_and_weights_from_expression
from nexinfosys.ie_exports.xml_export import export_model_to_xml
from nexinfosys.model_services import get_case_study_registry_objects, State
from nexinfosys.models import CodeImmutable
from nexinfosys.models.musiasem_concepts import ProblemStatement, Parameter, FactorsRelationDirectedFlowObservation, \
    FactorsRelationScaleObservation, Processor, FactorQuantitativeObservation, Factor, \
    ProcessorsRelationPartOfObservation, FactorType, Indicator, MatrixIndicator, IndicatorCategories, Benchmark
from nexinfosys.models.musiasem_concepts_helper import find_quantitative_observations
from nexinfosys.models.statistical_datasets import Dataset, Dimension, CodeList
from nexinfosys.solving.graph.computation_graph import ComputationGraph
from nexinfosys.solving.graph.flow_graph import FlowGraph, IType


class SolvingException(Exception):
    pass


class Computed(Enum):
    No = 1
    Yes = 2


class ComputationSource(Enum):
    Flow = 1
    Scale = 2
    ScaleChange = 3
    PartOfAggregation = 4
    InterfaceTypeAggregation = 5


class FloatComputedTuple(NamedTuple):
    value: FloatExp
    computed: Computed
    observer: str = None
    computation_source: ComputationSource = None


class ConflictResolution(Enum):
    No = 1
    Taken = 2
    Dismissed = 3


class ConflictingDataResolutionPolicy(Enum):
    TakeUpper = 1
    TakeLowerAggregation = 2

    @staticmethod
    def get_key():
        return "NISSolverConflictingDataResolutionPolicy"

    def resolve(self, computed_value: FloatComputedTuple, existing_value: FloatComputedTuple) \
            -> Tuple[FloatComputedTuple, FloatComputedTuple]:

        if self == self.TakeLowerAggregation:
            # Take computed aggregation over existing value
            return computed_value, existing_value
        elif self == self.TakeUpper:
            # Take existing value over computed aggregation
            return existing_value, computed_value


class MissingValueResolutionPolicy(Enum):
    UseZero = 0
    Invalidate = 1

    @staticmethod
    def get_key():
        return "NISSolverMissingValueResolutionPolicy"


class InterfaceNode:
    """
    Identifies an interface which value should be computed by the solver.
    An interface can be identified in two different ways:
    1. In the common case there is an interface declared in the Interfaces command. The interface is identified
       with "ProcessorName:InterfaceName".
    2. When we are aggregating by the interface type and there isn't a declared interface. The interface is
       identified with "ProcessorName:InterfaceTypeName:Orientation"
    """
    def __init__(self, interface_or_type: Union[Factor, FactorType], processor: Optional[Processor] = None,
                 orientation: Optional[str] = None, processor_name: Optional[str] = None):
        if isinstance(interface_or_type, Factor):
            self.interface: Optional[Factor] = interface_or_type
            self.interface_type = self.interface.taxon
            self.orientation: Optional[str] = orientation if orientation else self.interface.orientation
            self.interface_name: str = interface_or_type.name
            self.processor = processor if processor else self.interface.processor
        elif isinstance(interface_or_type, FactorType):
            self.interface: Optional[Factor] = None
            self.interface_type = interface_or_type
            self.orientation = orientation
            self.interface_name: str = ""
            self.processor = processor
        else:
            raise Exception(f"Invalid object type '{type(interface_or_type)}' for the first parameter. "
                            f"Valid object types are [Factor, FactorType].")

        self.processor_name: str = self.processor.full_hierarchy_name if self.processor else processor_name

    @property
    def key(self) -> Tuple:
        return self.processor_name, self.interface_name

    @property
    def alternate_key(self) -> Tuple:
        return self.processor_name, self.type, self.orientation

    @property
    def full_key(self) -> Tuple:
        return self.processor_name, self.interface_name, self.type, self.orientation

    @staticmethod
    def full_key_labels() -> List[str]:
        return ["Processor", "Interface", "InterfaceType", "Orientation"]

    @property
    def name(self) -> str:
        if self.interface_name:
            return ":".join(self.key)
        else:
            return ":".join(self.alternate_key)

    @property
    def type(self) -> str:
        return self.interface_type.name

    @property
    def unit(self):
        return self.interface_type.unit

    @property
    def roegen_type(self):
        if self.interface and self.interface.roegen_type:
            if isinstance(self.interface.roegen_type, str):
                return self.interface.roegen_type
            else:
                return self.interface.roegen_type.name.title()
        elif self.interface_type and self.interface_type.roegen_type:
            if isinstance(self.interface_type.roegen_type, str):
                return self.interface_type.roegen_type
            else:
                return self.interface_type.roegen_type.name.title()
        else:
            return ""

    @property
    def sphere(self) -> Optional[str]:
        if self.interface and self.interface.sphere:
            return self.interface.sphere
        else:
            return self.interface_type.sphere

    @property
    def system(self) -> Optional[str]:
        return self.processor.processor_system if self.processor else None

    @property
    def subsystem(self) -> Optional[SubsystemType]:
        return SubsystemType.from_str(self.processor.subsystem_type) if self.processor else None

    def has_interface(self) -> bool:
        return self.interface is not None

    def no_interface_copy(self) -> "InterfaceNode":
        return InterfaceNode(self.interface_type, self.processor, self.orientation)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return istr(str(self))

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other):
        return self.name < other.name


class ResultKey(NamedTuple):
    scenario: str
    period: str
    scope: Scope
    conflict_partof: ConflictResolution = ConflictResolution.No
    conflict_itype: ConflictResolution = ConflictResolution.No

    def as_string_tuple(self) -> Tuple[str, str, str, str, str]:
        return self.scenario, self.period, self.scope.name, self.conflict_partof.name, self.conflict_itype.name


ProcessorsRelationWeights = Dict[Tuple[Processor, Processor], Any]
InterfaceNodeHierarchy = Dict[InterfaceNode, Set[InterfaceNode]]

NodeFloatDict = Dict[InterfaceNode, FloatExp]
NodeFloatComputedDict = Dict[InterfaceNode, FloatComputedTuple]
ResultDict = Dict[ResultKey, NodeFloatComputedDict]

AstType = Dict
ObservationListType = List[Tuple[Optional[Union[float, AstType]], FactorQuantitativeObservation]]
TimeObservationsType = Dict[str, ObservationListType]
InterfaceNodeAstDict = Dict[InterfaceNode, Tuple[AstType, FactorQuantitativeObservation]]


def get_circular_dependencies(parameters: Dict[str, Tuple[Any, list]]) -> list:
    # Graph, for evaluation of circular dependencies
    G = nx.DiGraph()
    for param, (_, dependencies) in parameters.items():
        for param2 in dependencies:
            G.add_edge(param2, param)  # We need "param2" to obtain "param"
    return list(nx.simple_cycles(G))


def evaluate_parameters_for_scenario(base_params: List[Parameter], scenario_params: Dict[str, str]):
    """
    Obtain a dictionary (parameter -> value), where parameter is a string and value is a literal: number, boolean,
    category or string.

    Start from the base parameters then overwrite with the values in the current scenario.

    Parameters may depend on other parameters, so this has to be considered before evaluation.
    No cycles are allowed in the dependencies, i.e., if P2 depends on P1, P1 cannot depend on P2.
    To analyze this, first expressions are evaluated, extracting which parameters appear in each of them. Then a graph
    is elaborated based on this information. Finally, an algorithm to find cycles is executed.

    :param base_params:
    :param scenario_params:
    :return:
    """
    # Create dictionary without evaluation
    result_params = create_dictionary()
    result_params.update({p.name: p.default_value for p in base_params if p.default_value is not None})
    param_types = create_dictionary()
    param_types.update({p.name: p.type for p in base_params})

    # Overwrite with scenario expressions or constants
    result_params.update(scenario_params)

    state = State()
    known_params = create_dictionary()
    unknown_params = create_dictionary()

    # Now, evaluate ALL expressions
    for param, expression in result_params.items():
        ptype = param_types[param]
        if strcmp(ptype, "Number") or strcmp(ptype, "Boolean"):
            value, ast, params, issues = evaluate_numeric_expression_with_parameters(expression, state)
            if value is None:  # It is not a constant, store the parameters on which this depends
                unknown_params[param] = (ast, set([istr(p) for p in params]))
            else:  # It is a constant, store it
                result_params[param] = value  # Overwrite
                known_params[param] = value
        elif strcmp(ptype, "Code") or strcmp(ptype, "String"):
            result_params[param] = expression
            known_params[param] = expression

    cycles = get_circular_dependencies(unknown_params)
    if len(cycles) > 0:
        raise SolvingException(
            f"Parameters cannot have circular dependencies. {len(cycles)} cycles were detected: {':: '.join(cycles)}")

    # Initialize state with known parameters
    state.update(known_params)

    known_params_set = set([istr(p) for p in known_params.keys()])
    # Loop until no new parameters can be evaluated
    previous_len_unknown_params = len(unknown_params) + 1
    while len(unknown_params) < previous_len_unknown_params:
        previous_len_unknown_params = len(unknown_params)

        for param in list(unknown_params):  # A list(...) is used because the dictionary can be modified inside
            ast, params = unknown_params[param]

            if params.issubset(known_params_set):
                value, _, _, issues = evaluate_numeric_expression_with_parameters(ast, state)
                if value is None:
                    raise SolvingException(
                        f"It should be possible to evaluate the parameter '{param}'. Issues: {', '.join(issues)}")
                else:
                    del unknown_params[param]
                    result_params[param] = value
                    # known_params[param] = value  # Not necessary
                    known_params_set.add(istr(param))
                    state.set(param, value)

    if len(unknown_params) > 0:
        raise SolvingException(f"Could not evaluate the following parameters: {', '.join(unknown_params)}")

    return result_params


def get_evaluated_observations_by_time(prd: PartialRetrievalDictionary) -> TimeObservationsType:
    """
        Get all interface observations (intensive or extensive) by time.
        Also resolve expressions without parameters. Cannot resolve expressions depending only on global parameters
        because some of them can be overridden by scenario parameters.

        Each evaluated observation is stored as a tuple:
        * First: the evaluated result as a float or the prepared AST
        * Second: the observation

    :param prd: the global objects dictionary
    :return: a time dictionary with a list of observation on each time
    """
    observations: TimeObservationsType = defaultdict(list)
    state = State()

    # Get all observations by time
    for observation in find_quantitative_observations(prd, processor_instances_only=True):

        # Try to evaluate the observation value
        value, ast, _, issues = evaluate_numeric_expression_with_parameters(observation.value, state)

        # Store: (Value, FactorQuantitativeObservation)
        time = observation.attributes["time"].lower()
        observations[time].append((ifnull(value, ast), observation))

    if len(observations) == 0:
        return {}

    # Check all time periods are consistent. All should be Year or Month, but not both.
    time_period_type = check_type_consistency_from_all_time_periods(list(observations.keys()))
    assert(time_period_type in ["year", "month"])

    # Remove generic period type and insert it into all specific periods. E.g. "Year" into "2010", "2011" and "2012"
    if time_period_type in observations:
        # Generic monthly ("Month") or annual ("Year") data
        periodic_observations = observations.pop(time_period_type)

        for time in observations:
            observations[time] += periodic_observations

    return observations


def evaluate_numeric_expression_with_parameters(expression: Union[float, str, dict], state: State) \
        -> Tuple[Optional[float], Optional[AstType], Set, List[str]]:

    issues: List[Tuple[int, str]] = []
    ast: Optional[AstType] = None
    value: Optional[float] = None
    params = set()

    if expression is None:
        value = None

    elif isinstance(expression, float):
        value = expression

    elif isinstance(expression, dict):
        ast = expression
        value, params = ast_evaluator(ast, state, None, issues)
        if value is not None:
            ast = None

    elif isinstance(expression, str):
        try:
            value = float(expression)
        except ValueError:
            # print(f"{expression} before")
            ast = string_to_ast(expression_with_parameters, expression)
            # print(f"{expression} after")
            value, params = ast_evaluator(ast, state, None, issues)
            if value is not None:
                ast = None

    else:
        issues.append((3, f"Invalid type '{type(expression)}' for expression '{expression}'"))

    return value, ast, params, [i[1] for i in issues]


def check_type_consistency_from_all_time_periods(time_periods: List[str]) -> str:
    """ Check if all time periods are of the same period type, either Year or Month:
         - general "Year" & specific year (YYYY)
         - general "Month" & specific month (mm-YYYY or YYYY-mm, separator can be any of "-/")

    :param time_periods:
    :return:
    """
    # Based on the first element we will check the rest of elements
    period = next(iter(time_periods))

    if period == "year" or is_year(period):
        period_type = "year"
        period_check = is_year
    elif period == "month" or is_month(period):
        period_type = "month"
        period_check = is_month
    else:
        raise SolvingException(f"Found invalid period type '{period}'")

    for time_period in time_periods:
        if time_period != period_type and not period_check(time_period):
            raise SolvingException(
                f"Found period type inconsistency: accepting '{period_type}' but found '{time_period}'")

    return period_type


def split_observations_by_relativeness(observations_by_time: TimeObservationsType) -> Tuple[TimeObservationsType, TimeObservationsType]:
    observations_by_time_norelative = defaultdict(list)
    observations_by_time_relative = defaultdict(list)
    for time, observations in observations_by_time.items():
        for value, obs in observations:
            if obs.is_relative:
                observations_by_time_relative[time].append((value, obs))
            else:
                observations_by_time_norelative[time].append((value, obs))

    return observations_by_time_norelative, observations_by_time_relative


def compute_graph_results(comp_graph: ComputationGraph,
                          existing_results: NodeFloatComputedDict,
                          previous_known_nodes: Set[InterfaceNode],
                          computation_source: ComputationSource) -> NodeFloatComputedDict:
    # Filter results in graph
    graph_params: NodeFloatDict = {k: v.value for k, v in existing_results.items() if k in comp_graph.nodes}

    # Obtain nodes without a value
    compute_nodes = comp_graph.nodes_not_in_container(graph_params)

    if len(compute_nodes) == 0:
        print("All nodes have a value. Nothing to solve.")
        return {}

    print(f"****** NODES: {comp_graph.nodes}")
    print(f"****** UNKNOWN NODES: {compute_nodes}")

    new_computed_nodes: Set[InterfaceNode] = {k for k in existing_results if k not in previous_known_nodes}
    conflicts = comp_graph.compute_conflicts(new_computed_nodes, previous_known_nodes)

    raise_error_if_conflicts(conflicts, graph_params, comp_graph.name)

    results, _ = comp_graph.compute_values(compute_nodes, graph_params)

    # Return only entries with a valid value and set the name
    return_values: NodeFloatComputedDict = {}
    for k, v in results.items():
        if v is not None:
            # v.name = k.name
            return_values[k] = FloatComputedTuple(v, Computed.Yes, computation_source=computation_source)

    return return_values


def raise_error_if_conflicts(conflicts: Dict[InterfaceNode, Set[InterfaceNode]], graph_params: NodeFloatDict, graph_name: str):
    conflict_strings: List[str] = []
    for param, conf_params in conflicts.items():
        if conf_params:
            conf_params_string = "{" + ', '.join([f"{p} ({graph_params[p]})" for p in conf_params]) + "}"
            conflict_strings.append(f"{param} ({graph_params[param]}) -> {conf_params_string}")

    if conflict_strings:
        raise SolvingException(f"There are conflicts in the '{graph_name}' computation graph: {', '.join(conflict_strings)}")


def create_interface_edges(edges: List[Tuple[Factor, Factor, Optional[str]]]) \
        -> Generator[Tuple[InterfaceNode, InterfaceNode, Dict], None, None]:
    for src, dst, weight in edges:
        src_node = InterfaceNode(src)
        dst_node = InterfaceNode(dst)
        if "Archetype" in [src.processor.instance_or_archetype, dst.processor.instance_or_archetype]:
            print(f"WARNING: excluding relation from '{src_node}' to '{dst_node}' because of Archetype processor")
        else:
            yield src_node, dst_node, dict(weight=weight)


def resolve_weight_expressions(graph_list: List[nx.DiGraph], state: State, raise_error=False) -> None:
    for graph in graph_list:
        for u, v, data in graph.edges(data=True):
            expression = data["weight"]
            if expression is not None and not isinstance(expression, FloatExp):
                value, ast, params, issues = evaluate_numeric_expression_with_parameters(expression, state)
                if raise_error and value is None:
                    raise SolvingException(
                        f"Cannot evaluate expression "
                        f"'{expression}' for weight from interface '{u}' to interface '{v}'. Params: {params}. "
                        f"Issues: {', '.join(issues)}"
                    )

                data["weight"] = ast if value is None else FloatExp(value, None, str(expression))


def resolve_partof_weight_expressions(weights: ProcessorsRelationWeights, state: State, raise_error=False) \
        -> ProcessorsRelationWeights:
    evaluated_weights: ProcessorsRelationWeights = {}

    for (parent, child), expression in weights.items():
        if expression is not None and not isinstance(expression, FloatExp):
            value, ast, params, issues = evaluate_numeric_expression_with_parameters(expression, state)
            if raise_error and value is None:
                raise SolvingException(
                    f"Cannot evaluate expression '{expression}' for weight from child processor '{parent}' "
                    f"to parent processor '{child}'. Params: {params}. Issues: {', '.join(issues)}"
                )

            evaluated_weights[(parent, child)] = ast if value is None else FloatExp(value, None, str(expression))

    return evaluated_weights


def create_scale_change_relations_and_update_flow_relations(relations_flow: nx.DiGraph, registry,
                                                            interface_nodes: Set[InterfaceNode]) -> nx.DiGraph:
    relations_scale_change = nx.DiGraph()

    edges = [(r.source_factor, r.target_factor, r.back_factor, r.weight, r.scale_change_weight)
             for r in registry.get(FactorsRelationDirectedFlowObservation.partial_key())
             if r.scale_change_weight is not None or r.back_factor is not None]

    for src, dst, bck, weight, scale_change_weight in edges:

        source_node = InterfaceNode(src)
        dest_node = InterfaceNode(dst)
        back_node = InterfaceNode(bck) if bck else None

        if "Archetype" in [src.processor.instance_or_archetype,
                           dst.processor.instance_or_archetype,
                           bck.processor.instance_or_archetype if bck else None]:
            print(f"WARNING: excluding relation from '{source_node}' to '{dest_node}' "
                  f"and back to '{back_node}' because of Archetype processor")
            continue

        hidden_node = InterfaceNode(src.taxon,
                                    processor_name=f"{src.processor.full_hierarchy_name}-"
                                                   f"{dst.processor.full_hierarchy_name}",
                                    orientation="Input/Output")

        relations_flow.add_edge(source_node, hidden_node, weight=weight)
        relations_scale_change.add_edge(hidden_node, dest_node, weight=scale_change_weight, add_reverse_weight="yes")
        if back_node:
            relations_scale_change.add_edge(hidden_node, back_node, weight=scale_change_weight, add_reverse_weight="yes")

        relations_scale_change.nodes[hidden_node]["add_split"] = "yes"

        real_dest_node = InterfaceNode(source_node.interface_type, dest_node.processor,
                                       orientation="Input" if source_node.orientation.lower() == "output" else "Output")

        # Check if synthetic interface is equal to an existing one
        matching_interfaces = [n for n in interface_nodes if n.alternate_key == real_dest_node.alternate_key]
        if len(matching_interfaces) == 1:
            real_dest_node = matching_interfaces[0]
        else:
            interface_nodes.add(real_dest_node)

        if relations_flow.has_edge(source_node, real_dest_node):
            # weight = relations_flow[source_node][real_dest_node]['weight']
            relations_flow.remove_edge(source_node, real_dest_node)
            # relations_flow.add_edge(source_node, hidden_node, weight=weight)  # This "weight" should be the same
            relations_flow.add_edge(hidden_node, real_dest_node, weight=1.0)

    return relations_scale_change


def convert_params_to_extended_interface_names(params: Set[str], obs: FactorQuantitativeObservation, registry) \
        -> Tuple[Dict[str, str], List[str], List[str]]:
    extended_interface_names: Dict[str, str] = {}
    unresolved_params: List[str] = []
    issues: List[str] = []

    for param in params:
        # Check if param is valid interface name
        interfaces: Sequence[Factor] = registry.get(Factor.partial_key(processor=obs.factor.processor, name=param))
        if len(interfaces) == 1:
            node = InterfaceNode(interfaces[0])
            extended_interface_names[param] = node.name
        else:
            unresolved_params.append(param)
            if len(interfaces) > 1:
                issues.append(f"Multiple interfaces with name '{param}' exist, "
                              f"rename them to uniquely identify the desired one.")
            else:  # len(interfaces) == 0
                issues.append(f"No global parameter or interface exist with name '{param}'.")

    return extended_interface_names, unresolved_params, issues


def replace_ast_variable_parts(ast: AstType, variable_conversion: Dict[str, str]) -> AstType:
    new_ast = deepcopy(ast)

    for term in new_ast['terms']:
        if term['type'] == 'h_var':
            variable = term['parts'][0]
            if variable in variable_conversion:
                term['parts'] = [variable_conversion[variable]]

    return new_ast


def resolve_observations_with_parameters(state: State, observations: ObservationListType,
                                         observers_priority_list: Optional[List[str]], registry) \
        -> Tuple[NodeFloatComputedDict, InterfaceNodeAstDict]:
    resolved_observations: NodeFloatComputedDict = {}
    unresolved_observations_with_interfaces: InterfaceNodeAstDict = {}

    for expression, obs in observations:
        interface_params: Dict[str, str] = {}
        obs_new_value: Optional[str] = None
        value, ast, params, issues = evaluate_numeric_expression_with_parameters(expression, state)
        if value is None:
            interface_params, params, issues = convert_params_to_extended_interface_names(params, obs, registry)
            if interface_params and not issues:
                ast = replace_ast_variable_parts(ast, interface_params)
                obs_new_value = replace_string_from_dictionary(obs.value, interface_params)
            else:
                raise SolvingException(
                    f"Cannot evaluate expression '{expression}' for observation at interface '{obs.factor.name}'. "
                    f"Params: {params}. Issues: {', '.join(issues)}"
                )

        # Get observer name
        observer_name = obs.observer.name if obs.observer else None

        if observer_name and observers_priority_list and observer_name not in observers_priority_list:
            raise SolvingException(
                f"The specified observer '{observer_name}' for the interface '{obs.factor.name}' has not been included "
                f"in the observers' priority list: {observers_priority_list}"
            )

        # Create node from the interface
        node = InterfaceNode(obs.factor)

        if node in resolved_observations or node in unresolved_observations_with_interfaces:
            previous_observer_name: str = resolved_observations[node].observer \
                if node in resolved_observations else unresolved_observations_with_interfaces[node][1].observer.name

            if observer_name is None and previous_observer_name is None:
                raise SolvingException(
                    f"Multiple observations exist for the 'same interface '{node.name}' without a specified observer."
                )
            elif not observers_priority_list:
                raise SolvingException(
                    f"Multiple observations exist for the same interface '{node.name}' but an observers' priority list "
                    f"has not been (correctly) defined: {observers_priority_list}"
                )
            elif not precedes_in_list(observers_priority_list, observer_name, previous_observer_name):
                # Ignore this observation because a higher priority observations has previously been set
                continue

        if interface_params:
            new_obs = deepcopy(obs)
            if obs_new_value is not None:
                new_obs.value = obs_new_value
            unresolved_observations_with_interfaces[node] = (ast, new_obs)
            resolved_observations.pop(node, None)
        else:
            resolved_observations[node] = FloatComputedTuple(FloatExp(value, node.name, obs_new_value),
                                                             Computed.No, observer_name)
            unresolved_observations_with_interfaces.pop(node, None)

    return resolved_observations, unresolved_observations_with_interfaces


def resolve_observations_with_interfaces(
        state: State, existing_unresolved_observations: InterfaceNodeAstDict, existing_results: NodeFloatComputedDict) \
        -> Tuple[NodeFloatComputedDict, InterfaceNodeAstDict]:
    state.update({k.name: v.value.val for k, v in existing_results.items()})
    results: NodeFloatComputedDict = {}
    unresolved_observations: InterfaceNodeAstDict = {}

    for node, (ast, obs) in existing_unresolved_observations.items():
        value, ast, params, issues = evaluate_numeric_expression_with_parameters(ast, state)
        if value is not None:
            observer_name = obs.observer.name if obs.observer else None
            results[node] = FloatComputedTuple(FloatExp(value, node.name, str(obs.value)), Computed.No, observer_name)
        else:
            unresolved_observations[node] = (ast, obs)

    return results, unresolved_observations


def compute_flow_and_scale_computation_graphs(state: State,
                                              relative_observations: ObservationListType,
                                              relations_flow: nx.DiGraph,
                                              relations_scale: nx.DiGraph,
                                              relations_scale_change: nx.DiGraph) \
        -> Tuple[ComputationGraph, ComputationGraph, ComputationGraph]:

    # Create a copy of the main relations structures that are modified with time-dependent values
    time_relations_flow = relations_flow.copy()
    time_relations_scale = relations_scale.copy()
    time_relations_scale_change = relations_scale_change.copy()

    # Add Processors internal -RelativeTo- relations (time dependent)
    # Transform relative observations into graph edges
    for expression, obs in relative_observations:
        time_relations_scale.add_edge(InterfaceNode(obs.relative_factor, obs.factor.processor),
                                      InterfaceNode(obs.factor),
                                      weight=expression)

    # Last pass to resolve weight expressions: expressions with parameters can be solved
    resolve_weight_expressions([time_relations_flow, time_relations_scale, time_relations_scale_change],
                               state, raise_error=True)

    # Create computation graphs
    comp_graph_flow = create_computation_graph_from_flows(time_relations_flow, time_relations_scale)
    comp_graph_flow.name = "Flow"
    comp_graph_scale = ComputationGraph(time_relations_scale, "Scale")
    comp_graph_scale_change = ComputationGraph(time_relations_scale_change, "Scale Change")

    return comp_graph_flow, comp_graph_scale, comp_graph_scale_change


def create_computation_graph_from_flows(relations_flow: nx.DiGraph, relations_scale: Optional[nx.DiGraph] = None) -> ComputationGraph:
    flow_graph = FlowGraph(relations_flow)
    comp_graph_flow, issues = flow_graph.get_computation_graph(relations_scale)

    for issue in issues:
        print(issue)

    error_issues = [e.description for e in issues if e.itype == IType.ERROR]
    if len(error_issues) > 0:
        raise SolvingException(f"The computation graph cannot be generated. Issues: {', '.join(error_issues)}")

    return comp_graph_flow


def compute_interfacetype_hierarchies(registry, interface_nodes: Set[InterfaceNode]) -> InterfaceNodeHierarchy:

    def compute(parent: FactorType):
        """ Recursive computation for a depth-first search """
        if parent in visited_interface_types:
            return

        for child in interface_types_parent_relations[parent]:
            if child in interface_types_parent_relations:
                compute(child)

            for processor in {p.processor for p in interface_nodes}:  # type: Processor
                for orientation in orientations:
                    child_interfaces = interfaces_dict.get(
                        (processor.full_hierarchy_name, child.name, orientation), {})
                    if child_interfaces:
                        parent_interface = InterfaceNode(parent, processor, orientation)

                        interfaces = interfaces_dict.get(parent_interface.alternate_key, [])
                        if len(interfaces) == 1:
                            # Replace "ProcessorName:InterfaceTypeName:Orientation" -> "ProcessorName:InterfaceName"
                            parent_interface = interfaces[0]
                        else:  # len(interfaces) != 1
                            interface_nodes.add(parent_interface)
                            interfaces_dict.setdefault(parent_interface.alternate_key, []).append(parent_interface)

                        hierarchies.setdefault(parent_interface, set()).update(child_interfaces)

        visited_interface_types.add(parent)

    # Get all different existing interface types with children interface types
    interface_types_parent_relations: Dict[FactorType, Set[FactorType]] = \
        {ft: ft.get_children() for ft in registry.get(FactorType.partial_key()) if len(ft.get_children()) > 0}

    # Get the list of interfaces for each combination
    interfaces_dict: Dict[Tuple[str, str, str], List[InterfaceNode]] = {}
    for interface in interface_nodes:
        interfaces_dict.setdefault(interface.alternate_key, []).append(interface)

    hierarchies: InterfaceNodeHierarchy = {}
    visited_interface_types: Set[FactorType] = set()

    # Iterate over all relations
    for parent_interface_type in interface_types_parent_relations:
        compute(parent_interface_type)

    return hierarchies


def compute_partof_hierarchies(registry, interface_nodes: Set[InterfaceNode]) \
        -> Tuple[InterfaceNodeHierarchy, ProcessorsRelationWeights]:

    def compute(parent: Processor):
        """ Recursive computation for a depth-first search """
        if parent in visited_processors:
            return

        for child in processor_partof_relations[parent]:
            if child in processor_partof_relations:
                compute(child)

            child_interface_nodes: List[InterfaceNode] = processor_interface_nodes.get(child, [])

            if child_interface_nodes and (parent, child) in behave_as_differences:
                # Remove interfaces from child that doesn't belong to behave_as_processor
                child_interface_nodes = [n for n in child_interface_nodes if n.interface_name not in behave_as_differences[(parent, child)]]

            # Add the interfaces of the child processor to the parent processor
            for child_interface_node in child_interface_nodes:
                parent_interface_node = InterfaceNode(child_interface_node.interface, parent)

                # Search parent_interface in Set of existing interface_nodes, it can have same name but different
                # combination of (type, orientation). For example, we define:
                # - interface "ChildProcessor:Water" as (BlueWater, Input)
                # - interface "ParentProcessor:Water" as (BlueWater, Output)
                # In this case aggregating child interface results in a conflict in parent
                if parent_interface_node in interface_nodes:
                    for interface_node in interface_nodes:
                        if interface_node == parent_interface_node:
                            if (interface_node.type, interface_node.orientation) != (parent_interface_node.type, parent_interface_node.orientation):
                                raise SolvingException(
                                    f"Interface '{parent_interface_node}' already defined with type <{parent_interface_node.type}> and orientation <{parent_interface_node.orientation}> "
                                    f"is being redefined with type <{interface_node.type}> and orientation <{interface_node.orientation}> when aggregating processor "
                                    f"<{child_interface_node.processor_name}> to parent processor <{parent_interface_node.processor_name}>. Rename either the child or the parent interface.")
                            break
                else:
                    interface_nodes.add(parent_interface_node)
                    processor_interface_nodes.setdefault(parent_interface_node.processor, []).append(parent_interface_node)

                hierarchies.setdefault(parent_interface_node, set()).add(child_interface_node)

        visited_processors.add(parent)

    # Get the -PartOf- processor relations of the system
    processor_partof_relations, weights, behave_as_dependencies = get_processor_partof_relations(registry)

    # Get the list of interfaces of each processor
    processor_interface_nodes: Dict[Processor, List[InterfaceNode]] = {}
    for node in interface_nodes:
        processor_interface_nodes.setdefault(node.processor, []).append(node)

    check_behave_as_dependencies(behave_as_dependencies, processor_interface_nodes)
    behave_as_differences = compute_behave_as_differences(behave_as_dependencies, processor_interface_nodes)

    hierarchies: InterfaceNodeHierarchy = {}
    visited_processors: Set[Processor] = set()

    # Iterate over all relations
    for parent_processor in processor_partof_relations:
        compute(parent_processor)

    return hierarchies, weights


def check_behave_as_dependencies(
        behave_as_dependencies: Dict[Tuple[Processor, Processor], Processor],
        processor_interface_nodes: Dict[Processor, List[InterfaceNode]]):
    """ Make a check for the 'BehaveAs' property that can be defined in the 'BareProcessors' command.
        If defined, all the interfaces of the 'BehaveAs' processor must be specified in the selected processor."""
    for (_, child_processor), behave_as_processor in behave_as_dependencies.items():
        child_interfaces = {n.interface_name for n in processor_interface_nodes[child_processor]}
        behave_as_interfaces = {n.interface_name for n in processor_interface_nodes[behave_as_processor]}
        difference_interfaces = behave_as_interfaces.difference(child_interfaces)
        if difference_interfaces:
            raise SolvingException(
                f"The processor '{child_processor.name}' cannot behave as processor '{behave_as_processor.name}' on "
                f"aggregations because it doesn't have these interfaces: {difference_interfaces}")


def compute_behave_as_differences(
        behave_as_dependencies: Dict[Tuple[Processor, Processor], Processor],
        processor_interface_nodes: Dict[Processor, List[InterfaceNode]]) -> Dict[Tuple[Processor, Processor], Set[str]]:
    """ Compute the difference in interfaces from a processor and the associated BehaveAs processor """
    behave_as_differences: Dict[Tuple[Processor, Processor], Set[str]] = {}
    for (parent_processor, child_processor), behave_as_processor in behave_as_dependencies.items():
        child_interfaces = {n.interface_name for n in processor_interface_nodes[child_processor]}
        behave_as_interfaces = {n.interface_name for n in processor_interface_nodes[behave_as_processor]}
        behave_as_differences[(parent_processor, child_processor)] = child_interfaces.difference(behave_as_interfaces)

    return behave_as_differences


def get_processor_partof_relations(glb_idx: PartialRetrievalDictionary) \
        -> Tuple[Dict[Processor, Set[Processor]], ProcessorsRelationWeights, Dict[Tuple[Processor, Processor], Processor]]:
    """ Get in a dictionary the -PartOf- processor relations, ignoring Archetype processors """
    relations: Dict[Processor, Set[Processor]] = {}
    weights: ProcessorsRelationWeights = {}
    behave_as_dependencies: Dict[Tuple[Processor, Processor], Processor] = {}

    for parent, child, weight, behave_as_processor in \
            [(r.parent_processor, r.child_processor, r.weight, r.behave_as)
             for r in glb_idx.get(ProcessorsRelationPartOfObservation.partial_key())
             if "Archetype" not in [r.parent_processor.instance_or_archetype, r.child_processor.instance_or_archetype]]:
        relations.setdefault(parent, set()).add(child)
        weights[(parent, child)] = weight
        if behave_as_processor:
            behave_as_dependencies[(parent, child)] = behave_as_processor

    return relations, weights, behave_as_dependencies


def compute_hierarchy_aggregate_results(
        tree: InterfaceNodeHierarchy, params: NodeFloatComputedDict,
        prev_computed_values: NodeFloatComputedDict,
        conflicting_data_policy: ConflictingDataResolutionPolicy,
        missing_values_policy: MissingValueResolutionPolicy,
        computation_source: ComputationSource,
        processors_relation_weights: ProcessorsRelationWeights = None) \
        -> Tuple[NodeFloatComputedDict, NodeFloatComputedDict, NodeFloatComputedDict]:

    def compute_node(node: InterfaceNode) -> Optional[FloatExp]:
        # If the node has already been computed return the value
        if new_values.get(node) is not None:
            return new_values[node].value

        # Make a depth-first search
        return_value: Optional[FloatExp]
        children_values: List[FloatExp.ValueWeightPair] = []
        invalidate_sum_children: bool = False
        sum_children: Optional[FloatExp] = None

        # Try to get the sum from children, if any
        for child in sorted(tree.get(node, {})):
            child_value = compute_node(child)
            if child_value is not None:
                weight: FloatExp = None if processors_relation_weights is None \
                                        else processors_relation_weights[(node.processor, child.processor)]

                children_values.append((child_value, weight))
            elif missing_values_policy == MissingValueResolutionPolicy.Invalidate:
                # Invalidate current children computation and stop evaluating following children
                invalidate_sum_children = True
                break

        if not invalidate_sum_children:
            sum_children = FloatExp.compute_weighted_addition(children_values)

        float_value = params.get(node)
        if sum_children is not None:
            # New value has been computed
            sum_children.name = node.name
            new_computed_value = FloatComputedTuple(sum_children, Computed.Yes, computation_source=computation_source)

            if float_value is not None:
                # Conflict here: applies strategy
                taken_conflicts[node], dismissed_conflicts[node] = \
                    conflicting_data_policy.resolve(new_computed_value, float_value)

                new_values[node] = taken_conflicts[node]
                return_value = taken_conflicts[node].value
            else:
                new_values[node] = new_computed_value
                return_value = new_computed_value.value
        else:
            # No value got from children, try to search in "params"
            return_value = float_value.value if float_value is not None else None

        return return_value

    new_values: NodeFloatComputedDict = {**prev_computed_values}  # All computed aggregations
    taken_conflicts: NodeFloatComputedDict = {}  # Taken values on conflicting nodes
    dismissed_conflicts: NodeFloatComputedDict = {}  # Dismissed values on conflicting nodes

    for parent_node in tree:
        compute_node(parent_node)

    return new_values, taken_conflicts, dismissed_conflicts


def init_processor_full_names(registry: PartialRetrievalDictionary):
    for processor in registry.get(Processor.partial_key()):
        processor.full_hierarchy_name = processor.full_hierarchy_names(registry)[0]


def flow_graph_solver(global_parameters: List[Parameter], problem_statement: ProblemStatement,
                      global_state: State, dynamic_scenario: bool) -> List[Issue]:
    """
    A solver using the graph composed by the interfaces and the relationships (flows, part-of, scale, change-of-scale and relative-to)

    :param global_parameters: Parameters including the default value (if defined)
    :param problem_statement: ProblemStatement object, with scenarios (parameters changing the default)
                              and parameters for the solver
    :param global_state:      All variables available: object model, registry, datasets (inputs and outputs), ...
    :param dynamic_scenario:  If "True" store results in datasets separated from "fixed" scenarios.
                              Also "problem_statement" MUST have only one scenario with the parameters.
    :return: List of Issues
    """
    try:
        issues: List[Issue] = []
        glb_idx, _, _, datasets, _ = get_case_study_registry_objects(global_state)
        init_processor_full_names(glb_idx)

        # Get available observations
        time_absolute_observations, time_relative_observations = \
            split_observations_by_relativeness(get_evaluated_observations_by_time(glb_idx))

        if len(time_absolute_observations) == 0:
            return [Issue(IType.WARNING, f"No absolute observations have been found. The solver has nothing to solve.")]

        # Get available interfaces
        interface_nodes: Set[InterfaceNode] = {InterfaceNode(i) for i in glb_idx.get(Factor.partial_key())}

        # Get hierarchies of processors and update interfaces to compute
        partof_hierarchies, partof_weights = compute_partof_hierarchies(glb_idx, interface_nodes)

        # Get hierarchies of interface types and update interfaces to compute
        interfacetype_hierarchies = compute_interfacetype_hierarchies(glb_idx, interface_nodes)

        relations_flow, relations_scale, relations_scale_change = \
            compute_flow_and_scale_relation_graphs(glb_idx, interface_nodes)

        total_results: ResultDict = {}

        for scenario_name, scenario_params in problem_statement.scenarios.items():  # type: str, Dict[str, Any]
            print(f"********************* SCENARIO: {scenario_name}")

            scenario_state = State(evaluate_parameters_for_scenario(global_parameters, scenario_params))

            scenario_partof_weights = resolve_partof_weight_expressions(partof_weights, scenario_state, raise_error=True)

            # Get scenario parameters
            observers_priority_list = parse_string_as_simple_ident_list(scenario_state.get('NISSolverObserversPriority'))
            conflicting_data_policy = ConflictingDataResolutionPolicy[scenario_state.get(ConflictingDataResolutionPolicy.get_key())]
            missing_value_policy = MissingValueResolutionPolicy[scenario_state.get(MissingValueResolutionPolicy.get_key())]

            missing_value_policies: List[MissingValueResolutionPolicy] = [MissingValueResolutionPolicy.Invalidate]
            if missing_value_policy == MissingValueResolutionPolicy.UseZero:
                missing_value_policies.append(MissingValueResolutionPolicy.UseZero)

            for time_period, absolute_observations in time_absolute_observations.items():
                print(f"********************* TIME PERIOD: {time_period}")

                aggregations: NodeFloatComputedDict = {}
                total_itype_taken_results: NodeFloatComputedDict = {}
                total_itype_dismissed_results: NodeFloatComputedDict = {}
                total_partof_taken_results: NodeFloatComputedDict = {}
                total_partof_dismissed_results: NodeFloatComputedDict = {}

                try:
                    comp_graph_flow, comp_graph_scale, comp_graph_scale_change = \
                        compute_flow_and_scale_computation_graphs(scenario_state, time_relative_observations[time_period],
                                                                  relations_flow,
                                                                  relations_scale,
                                                                  relations_scale_change)

                    # Get final results from the absolute observations
                    results, unresolved_observations_with_interfaces = \
                        resolve_observations_with_parameters(scenario_state, absolute_observations,
                                                             observers_priority_list, glb_idx)

                    # Initializations
                    flow_last_known_nodes = set()
                    scale_last_known_nodes = set()
                    scale_change_last_known_nodes = set()
                    iteration_number = 1

                    # START ITERATIVE SOLVING

                    # We first iterate with policy MissingValueResolutionPolicy.Invalidate trying to get as many results
                    # we can without supposing zero for missing values.
                    # Second, if specified in paramater "NISSolverMissingValueResolutionPolicy" we try to get further
                    # results with policy MissingValueResolutionPolicy.UseZero.
                    for missing_value_policy in missing_value_policies:
                        previous_len_results = len(results) - 1

                        # Iterate while the number of results is increasing
                        while len(results) > previous_len_results:
                            print(f"********************* Solving iteration: {iteration_number}")
                            previous_len_results = len(results)

                            new_results = compute_graph_results(comp_graph_flow, results, flow_last_known_nodes, ComputationSource.Flow)
                            results.update(new_results)
                            flow_last_known_nodes = set(results.keys())

                            new_results = compute_graph_results(comp_graph_scale, results, scale_last_known_nodes, ComputationSource.Scale)
                            results.update(new_results)
                            scale_last_known_nodes = set(results.keys())

                            new_results = compute_graph_results(comp_graph_scale_change, results, scale_change_last_known_nodes, ComputationSource.ScaleChange)
                            results.update(new_results)
                            scale_change_last_known_nodes = set(results.keys())

                            new_results, itype_taken_results, itype_dismissed_results = \
                                compute_hierarchy_aggregate_results(
                                    interfacetype_hierarchies, results, aggregations, conflicting_data_policy,
                                    missing_value_policy, ComputationSource.InterfaceTypeAggregation)

                            aggregations.update(new_results)
                            results.update(new_results)
                            total_itype_taken_results.update(itype_taken_results)
                            total_itype_dismissed_results.update(itype_dismissed_results)

                            new_results, partof_taken_results, partof_dismissed_results = \
                                compute_hierarchy_aggregate_results(
                                    partof_hierarchies, results, aggregations, conflicting_data_policy,
                                    missing_value_policy, ComputationSource.PartOfAggregation, scenario_partof_weights)

                            aggregations.update(new_results)
                            results.update(new_results)
                            total_partof_taken_results.update(partof_taken_results)
                            total_partof_dismissed_results.update(partof_dismissed_results)

                            if unresolved_observations_with_interfaces:
                                new_results, unresolved_observations_with_interfaces = \
                                    resolve_observations_with_interfaces(
                                        scenario_state, unresolved_observations_with_interfaces, results
                                    )
                                results.update(new_results)

                            iteration_number += 1

                    if unresolved_observations_with_interfaces:
                        issues.append(Issue(IType.WARNING, f"Scenario '{scenario_name}' - period '{time_period}'."
                                                           f"The following observations could not be evaluated: "
                                                           f"{[k for k in unresolved_observations_with_interfaces.keys()]}"))

                    issues.extend(check_unresolved_nodes_in_computation_graphs(
                        [comp_graph_flow, comp_graph_scale, comp_graph_scale_change], results))

                    # issues.extend(check_unresolved_nodes_in_aggregation_hierarchies(
                    #     interfacetype_hierarchies + partof_hierarchies, results))

                    current_results: ResultDict = {}
                    result_key = ResultKey(scenario_name, time_period, Scope.Total)

                    # Filter out conflicted results from TOTAL results
                    current_results[result_key] = {k: v for k, v in results.items()
                                                   if k not in total_itype_taken_results and k not in total_partof_taken_results}

                    if total_itype_taken_results:
                        current_results[result_key._replace(conflict_itype=ConflictResolution.Taken)] = total_itype_taken_results
                        current_results[result_key._replace(conflict_itype=ConflictResolution.Dismissed)] = total_itype_dismissed_results

                    if total_partof_taken_results:
                        current_results[result_key._replace(conflict_partof=ConflictResolution.Taken)] = total_partof_taken_results
                        current_results[result_key._replace(conflict_partof=ConflictResolution.Dismissed)] = total_partof_dismissed_results

                    hierarchical_structures = [
                        HierarchicalNodeStructure.from_flow_computation_graph(comp_graph_flow, True),
                        HierarchicalNodeStructure.from_partof_aggregation(partof_hierarchies, scenario_partof_weights),
                        HierarchicalNodeStructure.from_interfacetype_aggregation(interfacetype_hierarchies)]
                    additional_hierarchical_structure = HierarchicalNodeStructure.from_flow_computation_graph(comp_graph_flow, False)

                    internal_results, external_results = \
                        compute_internal_external_results(results, hierarchical_structures, additional_hierarchical_structure)

                    current_results[result_key._replace(scope=Scope.Internal)] = internal_results
                    current_results[result_key._replace(scope=Scope.External)] = external_results

                    total_results.update(current_results)

                except SolvingException as e:
                    return [Issue(IType.ERROR, f"Scenario '{scenario_name}' - period '{time_period}'. {e.args[0]}")]

        #
        # ---------------------- CREATE PD.DATAFRAMES PREVIOUS TO OUTPUT DATASETS  ----------------------
        #

        data = {result_key.as_string_tuple() + node.full_key:
                    {"RoegenType": node.roegen_type if node else "-",
                     "Value": float_computed.value.val,
                     "Computed": float_computed.computed.name,
                     "ComputationSource": float_computed.computation_source.name if float_computed.computation_source else None,
                     "Observer": float_computed.observer,
                     "Expression": str(float_computed.value.exp),
                     "Unit": node.unit if node else "-",
                     "Level": node.processor.attributes.get('level', '') if node else "-",
                     "System": node.system if node else "-",
                     "Subsystem": node.subsystem.name if node else "-",
                     "Sphere": node.sphere if node else "-"
                     }
                for result_key, node_floatcomputed_dict in total_results.items()
                for node, float_computed in node_floatcomputed_dict.items()}

        export_solver_data(datasets, data, dynamic_scenario, glb_idx, global_parameters, problem_statement)

        dataframe_sankey = compute_dataframe_sankey(total_results)
        dataset_name = "flow_graph_solution_sankey"
        datasets[dataset_name] = get_dataset(dataframe_sankey, dataset_name, "Flow Graph Solution - Sankey")

        return issues
    except SolvingException as e:
        traceback.print_exc()  # Print the Exception to std output
        return [Issue(IType.ERROR, e.args[0])]


def compute_dataframe_sankey(results: ResultDict) -> pd.DataFrame:
    data: List[Dict] = []
    for result_key, node_floatcomputed_dict in results.items():
        if result_key.scope == Scope.Total and result_key.conflict_itype != ConflictResolution.Dismissed \
           and result_key.conflict_partof != ConflictResolution.Dismissed:

            for node, float_computed in node_floatcomputed_dict.items():
                if float_computed.computed == Computed.Yes:
                    for interface_fullname, weight in get_interfaces_and_weights_from_expression(float_computed.value.exp):
                        data.append(
                            {"Scenario": result_key.scenario,
                             "Period": result_key.period,
                             "OriginProcessor": interface_fullname.split(":")[0],
                             "OriginInterface": interface_fullname.split(":")[1],
                             "DestinationProcessor": node.processor_name,
                             "DestinationInterface": node.interface_name if node.interface_name else node.type+":"+node.orientation,
                             "RelationType": float_computed.computation_source.name if float_computed.computation_source else None,
                             "Quantity": weight
                             }
                        )

    df = pd.DataFrame(data)
    df.set_index(["Scenario", "Period", "OriginProcessor", "OriginInterface", "DestinationProcessor", "DestinationInterface"], inplace=True)
    return df.sort_index()


def mark_observations_and_scales_as_internal_results(
        results: NodeFloatComputedDict, internal_results: NodeFloatComputedDict) -> NoReturn:
    for node, value in results.items():
        if (value.computed == Computed.No) or \
           (value.computation_source and value.computation_source == ComputationSource.Scale):
            internal_results[node] = deepcopy(value)


class HierarchicalNodeStructure:
    def __init__(self, structure: Union[ComputationGraph, InterfaceNodeHierarchy],
                 computation_source: ComputationSource,
                 weights: Optional[ProcessorsRelationWeights] = None,
                 direct: Optional[bool] = None):
        assert(isinstance(structure, ComputationGraph) or isinstance(structure, Dict))
        self.structure = structure
        self.computation_source = computation_source
        self.weights = weights
        self.direct = direct

    @classmethod
    def from_partof_aggregation(cls, structure: InterfaceNodeHierarchy, weights: ProcessorsRelationWeights) -> 'HierarchicalNodeStructure':
        return cls(structure, ComputationSource.PartOfAggregation, weights)

    @classmethod
    def from_interfacetype_aggregation(cls, structure: InterfaceNodeHierarchy) -> 'HierarchicalNodeStructure':
        return cls(structure, ComputationSource.InterfaceTypeAggregation)

    @classmethod
    def from_flow_computation_graph(cls, structure: ComputationGraph, direct: Optional[bool]) -> 'HierarchicalNodeStructure':
        return cls(structure, ComputationSource.Flow, direct=direct)

    def __iter__(self):
        if isinstance(self.structure, ComputationGraph):
            return (n for n in self.structure.nodes)
        else:
            return (n for n in self.structure)

    def get_children(self, node: InterfaceNode) -> List[Tuple[InterfaceNode, Optional[FloatExp]]]:
        if isinstance(self.structure, ComputationGraph):
            if self.direct:
                return self.structure.direct_inputs(node)
            else:
                return self.structure.reverse_inputs(node)
        else:
            if node in self.structure:
                if self.weights:
                    return [(n, self.weights[(node.processor, n.processor)]) for n in self.structure[node]]
                else:
                    return [(n, None) for n in self.structure[node]]
            else:
                return []


def compute_internal_external_results(results: NodeFloatComputedDict, structures: List[HierarchicalNodeStructure],
                                      additional_structure: HierarchicalNodeStructure) \
        -> Tuple[NodeFloatComputedDict, NodeFloatComputedDict]:

    def compute_structures() -> int:
        unknown_nodes: Set[InterfaceNode] = set()
        for structure in structures:
            unknown_nodes |= compute_hierarchical_structure_internal_external_results(structure, results,
                                                                                      internal_results,
                                                                                      external_results)
        return len(unknown_nodes)

    internal_results: NodeFloatComputedDict = {}
    external_results: NodeFloatComputedDict = {}

    mark_observations_and_scales_as_internal_results(results, internal_results)

    len_unknown = len(results)
    prev_len_unknown = len_unknown + 1
    while len_unknown and len_unknown < prev_len_unknown:
        prev_len_unknown = len_unknown

        len_unknown = compute_structures()

        # If resolution is stuck try to solve flow graph in reverse order
        if len_unknown and len_unknown == prev_len_unknown:
            compute_hierarchical_structure_internal_external_results(additional_structure, results,
                                                                     internal_results, external_results)
            len_unknown = compute_structures()

    return internal_results, external_results


def compute_hierarchical_structure_internal_external_results(
        structure: HierarchicalNodeStructure,
        results: NodeFloatComputedDict,
        internal_results: NodeFloatComputedDict, external_results: NodeFloatComputedDict) -> Set[InterfaceNode]:

    def compute(node: InterfaceNode) -> Tuple[Optional[FloatComputedTuple], Optional[FloatComputedTuple]]:
        if node not in internal_results and node not in external_results:
            if not structure.get_children(node):
                unknown_nodes.add(node)
                return None, None
            else:
                internal_addends: List[FloatExp.ValueWeightPair] = []
                external_addends: List[FloatExp.ValueWeightPair] = []

                for child_node, weight in sorted(structure.get_children(node)):
                    child_value = deepcopy(results[child_node])
                    same_system = node.system == child_node.system and node.subsystem.is_same_scope(child_node.subsystem)
                    if same_system:
                        child_internal_value, child_external_value = compute(child_node)

                        if not child_internal_value and not child_external_value:
                            unknown_nodes.add(node)
                            return None, None

                        if child_internal_value:
                            child_internal_value.value.name = Scope.Internal.name + brackets(child_node.name)
                            internal_addends.append((child_internal_value.value, weight))

                        if child_external_value:
                            child_external_value.value.name = Scope.External.name + brackets(child_node.name)
                            external_addends.append((child_external_value.value, weight))
                    else:
                        external_addends.append((child_value.value, weight))

                if internal_addends:
                    scope_value = FloatExp.compute_weighted_addition(internal_addends)
                    scope_value.name = node.name
                    internal_results[node] = FloatComputedTuple(scope_value, Computed.Yes,
                                                                computation_source=structure.computation_source)

                if external_addends:
                    scope_value = FloatExp.compute_weighted_addition(external_addends)
                    scope_value.name = node.name
                    external_results[node] = FloatComputedTuple(scope_value, Computed.Yes,
                                                                computation_source=structure.computation_source)

        return internal_results.get(node), external_results.get(node)

    unknown_nodes: Set[InterfaceNode] = set()
    for node in structure:
        compute(node)

    return unknown_nodes


def check_unresolved_nodes_in_computation_graphs(computation_graphs: List[ComputationGraph], resolved_nodes: NodeFloatComputedDict) -> List[Issue]:
    issues: List[Issue] = []
    for comp_graph in computation_graphs:
        unresolved_nodes = [n for n in comp_graph.nodes if n not in resolved_nodes]
        if unresolved_nodes:
            issues.append(Issue(IType.WARNING, f"The following nodes in '{comp_graph.name}' graph could not be "
                                               f"evaluated: {unresolved_nodes}"))
    return issues


def check_unresolved_nodes_in_aggregation_hierarchies(hierarchies: List[InterfaceNodeHierarchy], resolved_nodes: NodeFloatComputedDict) -> List[Issue]:
    issues: List[Issue] = []
    unresolved_nodes: Set[InterfaceNode] = set()

    for hierarchy in hierarchies:
        unresolved_nodes.update({n for n in hierarchy if n not in resolved_nodes})
        for parent, children in hierarchy.items():
            unresolved_nodes.update({n for n in children if n not in resolved_nodes})

    if unresolved_nodes:
        issues.append(Issue(IType.WARNING, f"The following nodes in aggregation hierarchies could not be "
                                           f"evaluated: {unresolved_nodes}"))
    return issues


def compute_flow_and_scale_relation_graphs(registry, interface_nodes: Set[InterfaceNode]):

    # Compute Interfaces -Flow- relations (time independent)
    relations_flow = nx.DiGraph(
        incoming_graph_data=create_interface_edges(
            [(r.source_factor, r.target_factor, r.weight)
             for r in registry.get(FactorsRelationDirectedFlowObservation.partial_key())
             if r.scale_change_weight is None and r.back_factor is None]
        )
    )
    # Compute Processors -Scale- relations (time independent)
    relations_scale = nx.DiGraph(
        incoming_graph_data=create_interface_edges(
            [(r.origin, r.destination, r.quantity)
             for r in registry.get(FactorsRelationScaleObservation.partial_key())]
        )
    )

    # Compute Interfaces -Scale Change- relations (time independent). Also update Flow relations.
    relations_scale_change = create_scale_change_relations_and_update_flow_relations(relations_flow, registry, interface_nodes)

    # First pass to resolve weight expressions: only expressions without parameters can be solved
    # NOT WORKING:
    # 1) the method ast_evaluator() doesn't get global Parameters,
    # 2) the expression for the FloatExp() is not correctly computed on a second pass
    # resolve_weight_expressions([relations_flow, relations_scale, relations_scale_change], state)

    return relations_flow, relations_scale, relations_scale_change


def export_solver_data(datasets, data, dynamic_scenario, glb_idx, global_parameters, problem_statement) -> NoReturn:
    df = pd.DataFrame.from_dict(data, orient='index')

    # Round all values to 3 decimals
    df = df.round(3)
    # Give a name to the dataframe indexes
    index_names = [f.title() for f in
                   ResultKey._fields] + InterfaceNode.full_key_labels()
    df.index.names = index_names
    # Sort the dataframe based on indexes. Not necessary, only done for debugging purposes.
    df = df.sort_index(level=index_names)

    # print(df)

    # Create Matrix to Sankey graph
    ds_flow_values = prepare_sankey_dataset(glb_idx, df)

    # Convert model to XML and to DOM tree. Used by XPath expressions (Matrices and Global Indicators)
    _, p_map = export_model_to_xml(glb_idx)  # p_map: {(processor_full_path_name, Processor), ...}
    dom_tree = etree.fromstring(_).getroottree()  # dom_tree: DOM against which an XQuery can be executed

    # Obtain Analysis objects: Indicators and Benchmarks
    indicators = glb_idx.get(Indicator.partial_key())
    matrix_indicators = glb_idx.get(MatrixIndicator.partial_key())
    benchmarks = glb_idx.get(Benchmark.partial_key())

    # Filter out conflicts and prepare for case insensitiveness
    # Filter: Conflict_Partof!='Dismissed', Conflic_iType!='Dismissed', and remove the two columns
    df_without_conflicts = get_conflicts_filtered_dataframe(df)
    inplace_case_sensitiveness_dataframe(df_without_conflicts)

    # Calculate ScalarIndicators (Local and Global)
    df_local_indicators = calculate_local_scalar_indicators(indicators, dom_tree, p_map, df_without_conflicts, global_parameters, problem_statement)
    df_global_indicators = calculate_global_scalar_indicators(indicators, dom_tree, p_map, df_without_conflicts, df_local_indicators, global_parameters, problem_statement)

    # Calculate benchmarks
    ds_benchmarks = calculate_local_benchmarks(df_local_indicators, indicators)  # Find local indicators, and related benchmarks (indic_to_benchmarks). For each group (scenario, time, scope, processor): for each indicator, frame the related benchmark and add the framing result
    ds_global_benchmarks = calculate_global_benchmarks(df_global_indicators, indicators)  # Find global indicators, and related benchmarks (indic_to_benchmarks). For each group (scenario, time, scope, processor): for each indicator, frame the related benchmark and add the framing result

    # Prepare Benchmarks to Stakeholders DataFrame
    ds_stakeholders = prepare_benchmarks_to_stakeholders(benchmarks)  # Find all benchmarks. For each benchmark, create a row per stakeholder -> return the dataframe

    # Prepare Matrices
    # TODO df_attributes
    matrices = prepare_matrix_indicators(matrix_indicators, glb_idx, dom_tree, p_map, df, df_local_indicators, dynamic_scenario)

    #
    # ---------------------- CREATE DATASETS AND STORE IN STATE ----------------------
    #

    if not dynamic_scenario:
        ds_name = "flow_graph_solution"
        ds_flows_name = "flow_graph_solution_edges"
        ds_indicators_name = "flow_graph_solution_indicators"
        df_global_indicators_name = "flow_graph_global_indicators"
        ds_benchmarks_name = "flow_graph_solution_benchmarks"
        ds_global_benchmarks_name = "flow_graph_solution_global_benchmarks"
        ds_stakeholders_name = "benchmarks_and_stakeholders"
    else:
        ds_name = "dyn_flow_graph_solution"
        ds_flows_name = "dyn_flow_graph_solution_edges"
        ds_indicators_name = "dyn_flow_graph_solution_indicators"
        df_global_indicators_name = "dyn_flow_graph_global_indicators"
        ds_benchmarks_name = "dyn_flow_graph_solution_benchmarks"
        ds_global_benchmarks_name = "dyn_flow_graph_solution_global_benchmarks"
        ds_stakeholders_name = "benchmarks_and_stakeholders"

    for d, name, label in [(df, ds_name, "Flow Graph Solver - Interfaces"),
                           (ds_flow_values, ds_flows_name, "Flow Graph Solver Edges - Interfaces"),
                           (df_local_indicators, ds_indicators_name, "Flow Graph Solver - Local Indicators"),
                           (df_global_indicators, df_global_indicators_name, "Flow Graph Solver - Global Indicators"),
                           (ds_benchmarks, ds_benchmarks_name, "Flow Graph Solver - Local Benchmarks"),
                           (ds_global_benchmarks, ds_global_benchmarks_name, "Flow Graph Solver - Global Benchmarks"),
                           (ds_stakeholders, ds_stakeholders_name, "Benchmarks - Stakeholders")
                           ]:
        if not d.empty:
            datasets[name] = get_dataset(d, name, label)

    # Register matrices
    for n, ds in matrices.items():
        datasets[n] = ds

    # Create dataset and store in State (specific of "Biofuel case study")
    # datasets["end_use_matrix"] = get_eum_dataset(df)

    return []


def prepare_benchmarks_to_stakeholders(benchmarks: List[Benchmark]):
    rows = []
    for b in benchmarks:
        for s in b.stakeholders:
            rows.append((b.name, s))

    df = pd.DataFrame(data=rows, columns=["Benchmark", "Stakeholder"])
    df.set_index("Benchmark", inplace=True)
    return df


def add_conflicts_to_results(existing_results: ResultDict, taken_results: ResultDict, dismissed_results: ResultDict,
                             conflict_type: str) -> ResultDict:
    """ Iterate on the existing results and mark which of them have been involved into a conflict """
    results: ResultDict = {}
    for result_key, node_floatcomputed_dict in existing_results.items():

        if result_key in taken_results:
            assert result_key in dismissed_results
            key_taken = result_key._replace(**{conflict_type: ConflictResolution.Taken})
            key_dismissed = result_key._replace(**{conflict_type: ConflictResolution.Dismissed})

            for node, float_computed in node_floatcomputed_dict.items():
                if node in taken_results[result_key]:
                    results.setdefault(key_taken, {})[node] = taken_results[result_key][node]
                    results.setdefault(key_dismissed, {})[node] = dismissed_results[result_key][node]
                else:
                    results.setdefault(result_key, {})[node] = float_computed
        else:
            results[result_key] = node_floatcomputed_dict

    return results


def prepare_sankey_dataset(registry: PartialRetrievalDictionary, df: pd.DataFrame):
    # Create Matrix to Sankey graph

    FactorsRelationDirectedFlowObservation_list = registry.get(FactorsRelationDirectedFlowObservation.partial_key())

    ds_flows = pd.DataFrame({'source': [i._source.full_name for i in FactorsRelationDirectedFlowObservation_list],
                             'source_processor': [i._source._processor._name for i in
                                                  FactorsRelationDirectedFlowObservation_list],
                             'source_level': [i._source._processor._attributes['level'] if (
                                         'level' in i._source._processor._attributes) else None for i in
                                              FactorsRelationDirectedFlowObservation_list],
                             'target': [i._target.full_name for i in FactorsRelationDirectedFlowObservation_list],
                             'target_processor': [i._target._processor._name for i in
                                                  FactorsRelationDirectedFlowObservation_list],
                             'target_level': [i._target._processor._attributes[
                                                  'level'] if 'level' in i._target._processor._attributes else None for
                                              i in FactorsRelationDirectedFlowObservation_list],
                             # 'RoegenType_target': [i.target_factor._attributes['roegen_type']for i in FactorsRelationDirectedFlowObservation_list],
                             'Sphere_target': [i.target_factor._attributes['sphere'] for i in
                                               FactorsRelationDirectedFlowObservation_list],
                             'Subsystem_target': [i._target._processor._attributes['subsystem_type'] for i in
                                                  FactorsRelationDirectedFlowObservation_list],
                             'System_target': [i._target._processor._attributes['processor_system'] for i in
                                               FactorsRelationDirectedFlowObservation_list]
                             }
                            )

    # I suppose that relations between processors (source-target) doesn't change between different scenarios.
    df2 = df.reset_index()
    processor = df2["Processor"].apply(lambda x: x.split("."))
    df2["lastprocessor"] = [i[-1] for i in processor]
    df2["source"] = df2["lastprocessor"] + ":" + df2["Interface"]
    # df2 = df2[df2["Orientation"]=="Output"] It is not necessary?

    ds_flow_values = pd.merge(df2, ds_flows, on="source")
    ds_flow_values = ds_flow_values.drop(
        columns=["Orientation", "lastprocessor", "Processor", "Interface", 'RoegenType'], axis=1)
    ds_flow_values = ds_flow_values.rename(
        columns={'Sphere': 'Sphere_source', 'System': 'System_source', 'Subsystem': 'Subsystem_source'})
    # ds_flow_values.reset_index()
    # if not ds_flows.empty:

    return ds_flow_values


def get_conflicts_filtered_dataframe(in_df: pd.DataFrame) -> pd.DataFrame:
    filt = in_df.index.get_level_values("Conflict_Partof").isin(["No", "Taken"]) & in_df.index.get_level_values(
        "Conflict_Itype").isin(["No", "Taken"])
    df = in_df[filt]
    df = df.droplevel("Conflict_Partof")
    df = df.droplevel("Conflict_Itype")
    return df


def inplace_case_sensitiveness_dataframe(df: pd.DataFrame):
    if not case_sensitive:
        level_processor = df.index._get_level_number("Processor")
        level_interface = df.index._get_level_number("Interface")
        df.index.set_levels([df.index.levels[level_processor].str.lower(),
                             df.index.levels[level_interface].str.lower()],
                            level=[level_processor, level_interface],
                            verify_integrity=False,
                            inplace=True)


def calculate_local_scalar_indicators(indicators: List[Indicator],
                                      serialized_model: lxml.etree._ElementTree,
                                      p_map: Dict[str, Processor],
                                      results: pd.DataFrame,
                                      global_parameters: List[Parameter], problem_statement: ProblemStatement) -> pd.DataFrame:
    """
    Compute local scalar indicators using data from "results", and return a pd.DataFrame

    :param indicators: List of indicators to compute
    :param serialized_model:
    :param p_map:
    :param results: Result of the graph solving process ("flow_graph_solution")
    :param global_parameters: List of parameter definitions
    :param problem_statement: Object with a list of scenarios (defining Parameter sets)
    :return: pd.DataFrame with all the local indicators
    """

    # The "columns" in the index of "results" are:
    # 'Scenario', 'Period', 'Scope', 'Processor', 'Interface', 'Orientation'
    # Group by: 'Scenario', 'Period', 'Scope', 'Processor'
    # Rearrange: 'Interface' and 'Orientation'
    idx_names = ["Scenario", "Period", "Scope", "Processor"]  # Changing factors

    def calculate_local_scalar_indicator(indicator: Indicator) -> pd.DataFrame:
        """

        :param indicator:
        :return:
        """

        df = results

        # Parse the expression
        ast = string_to_ast(indicator_expression, indicator.formula if case_sensitive else indicator.formula.lower())

        # Scenario parameters
        scenario_params = create_dictionary()
        for scenario_name, scenario_exp_params in problem_statement.scenarios.items():  # type: str, dict
            scenario_params[scenario_name] = evaluate_parameters_for_scenario(global_parameters, scenario_exp_params)

        issues = []
        new_df_rows_idx = []
        new_df_rows_data = []
        for t, g in df.groupby(idx_names):  # "t", the current tuple; "g", the values of the group
            params = scenario_params[t[0]]
            # Elaborate a dictionary with: <interface>_<orientation>: <Value>
            d = {}
            # Iterate through available values in a single processor
            for row, sdf in g.iterrows():
                iface = sdf["Interface"]
                iface_orientation = iface + "_" + sdf["Orientation"]
                if iface_orientation in d:
                    print(f"{iface_orientation} found to already exist!")
                d[iface_orientation] = sdf["Value"]
                if iface not in d:
                    d[iface] = sdf["Value"]  # First appearance allowed, insert, others ignored
            # Include parameters (with priority)
            d.update(params)
            if not case_sensitive:
                d = {k.lower(): v for k, v in d.items()}

            state = State(d)
            val, variables = ast_evaluator(ast, state, None, issues)
            if val is not None:  # If it was possible to evaluate ... append a new row
                l = list(t)
                l.append(indicator.name)
                t = tuple(l)
                new_df_rows_idx.append(t)  # (scenario, period, scope, processor)
                new_df_rows_data.append((val, None))  # (indicator, value, unit)
        # print(issues)
        # Construct pd.DataFrame with the result of the scalar indicator calculation
        df2 = pd.DataFrame(data=new_df_rows_data,
                           index=pd.MultiIndex.from_tuples(new_df_rows_idx, names=idx_names+["Indicator"]),
                           columns=["Value", "Unit"])
        return df2

    # -- calculate_local_scalar_indicators --
    idx_to_change = ["Interface"]
    results.reset_index(idx_to_change, inplace=True)

    # For each ScalarIndicator...
    dfs = []
    for si in indicators:
        if si._indicator_category == IndicatorCategories.factors_expression:
            dfi = calculate_local_scalar_indicator(si)
            if not dfi.empty:
                dfs.append(dfi)

    # Restore index
    results.set_index(idx_to_change, append=True, inplace=True)

    if dfs:
        return pd.concat(dfs)
    else:
        return pd.DataFrame()


def calculate_global_scalar_indicators(indicators: List[Indicator],
                                      serialized_model: lxml.etree._ElementTree, p_map: Dict[str, Processor],
                                      results: pd.DataFrame, local_indicators: pd.DataFrame,
                                      global_parameters: List[Parameter], problem_statement: ProblemStatement) -> pd.DataFrame:
    """
    Compute global scalar indicators using data from "results", and return a pd.DataFrame

    :param indicators: List of indicators to compute
    :param serialized_model:
    :param p_map:
    :param results: Result of the graph solving process
    :param global_parameters: List of parameter definitions
    :param problem_statement: Object with a list of scenarios (defining Parameter sets)
    :return: pd.DataFrame with all the local indicators
    """

    # The "columns" in the index of "results" are:
    # 'Scenario', 'Period', 'Scope', 'Processor', 'Interface', 'Orientation'
    # Group by: 'Scenario', 'Period'
    # Aggregator function uses a "Processors selector" and a "Scope parameter"
    # Then, only one Interface(and its Orientation) allowed
    # Filter the passed group by processor and scope, by Interface and Orientation
    # Aggregate the Value column according of remaining rows
    idx_names = ["Scenario", "Period"]  # , "Scope"

    def calculate_global_scalar_indicator(indicator: Indicator) -> pd.DataFrame:
        """

        :param indicator:
        :return:
        """

        df = results

        # Parse the expression
        ast = string_to_ast(indicator_expression, indicator.formula if case_sensitive else indicator.formula.lower())

        # Scenario parameters
        scenario_params = create_dictionary()
        for scenario_name, scenario_exp_params in problem_statement.scenarios.items():  # type: str, dict
            scenario_params[scenario_name] = evaluate_parameters_for_scenario(global_parameters, scenario_exp_params)

        issues = []
        new_df_rows_idx = []
        new_df_rows_data = []
        for t, g in df.groupby(idx_names):  # GROUP BY Scenario, Period
            params = scenario_params[t[0]]  # Obtain parameter values from scenario, in t[0]
            # TODO Local indicators from the selected processors, for the selected Scenario, Period, Scope
            local_indicators_extract = pd.DataFrame()
            # TODO If a specific indicator or interface from a processor is mentioned, put it as a variable
            # Variables for aggregator functions (which should be present in the AST)
            d = dict(_processors_map=p_map,
                     _processors_dom=serialized_model,
                     _df_group=g,
                     _df_indicators_group=local_indicators_extract)
            # Include parameters (with priority)
            d.update(params)
            if not case_sensitive:
                d = {k.lower(): v for k, v in d.items()}

            state = State(d)
            val, variables = ast_evaluator(ast, state, None, issues, allowed_functions=global_functions_extended)

            if val is not None:
                new_df_rows_idx.append(t)  # (scenario, period)
                new_df_rows_data.append((indicator.name, val, None))
        print(issues)
        # Construct pd.DataFrame with the result of the scalar indicator calculation
        df2 = pd.DataFrame(data=new_df_rows_data,
                           index=pd.MultiIndex.from_tuples(new_df_rows_idx, names=idx_names),
                           columns=["Indicator", "Value", "Unit"])
        return df2

    # -- calculate_global_scalar_indicators --
    idx_to_change = []
    results.reset_index(idx_to_change, inplace=True)

    # For each ScalarIndicator...
    dfs = []
    for si in indicators:
        if si._indicator_category == IndicatorCategories.case_study:
            dfi = calculate_global_scalar_indicator(si)
            if not dfi.empty:
                dfs.append(dfi)

    # Restore index
    results.set_index(idx_to_change, append=True, inplace=True)

    if dfs:
        return pd.concat(dfs)
    else:
        return pd.DataFrame()


range_ast = {}


def get_benchmark_category(b: Benchmark, v):
    c = None
    for r in b.ranges.values():
        cat = r["category"]
        range = r["range"]
        if range in range_ast:
            ast = range_ast[range]
        else:
            ast = string_to_ast(number_interval, range)
            range_ast[range] = ast
        in_left = (ast["left"] == "[" and ast["number_left"] <= v) or (ast["left"] == "(" and ast["number_left"] < v)
        in_right = (ast["right"] == "]" and ast["number_right"] >= v) or (ast["right"] == ")" and ast["number_right"] > v)
        if in_left and in_right:
            c = cat
            break

    return c


def calculate_local_benchmarks(df_local_indicators, indicators: List[Indicator]):
    """
    From the dataframe of local indicators: scenario, period, scope, processor, indicator, value
    Prepare a dataframe with columns: scenario, period, scope, processor, indicator, benchmark, value

    :param df_local_indicators:
    :param indicators: List of all Indicators (inside it is filtered to process only Local Indicators)
    :return:
    """
    if df_local_indicators.empty:
        return pd.DataFrame()

    ind_map = create_dictionary()
    for si in indicators:
        if si._indicator_category == IndicatorCategories.factors_expression:
            if len(si.benchmarks) > 0:
                ind_map[si.name] = si

    idx_names = ["Scenario", "Period", "Scope", "Processor", "Indicator"]  # Changing factors

    new_df_rows_idx = []
    new_df_rows_data = []
    indicator_column_idx = 4
    value_column_idx = df_local_indicators.columns.get_loc("Value")
    unit_column_idx = df_local_indicators.columns.get_loc("Unit")
    for r in df_local_indicators.itertuples():
        ind = ind_map[r[0][indicator_column_idx]]
        val = r[1+value_column_idx]
        unit = r[1+unit_column_idx]
        for b in ind.benchmarks:
            c = get_benchmark_category(b, val)
            if not c:
                c = f"<out ({val})>"

            new_df_rows_idx.append(r[0])  # (scenario, period, scope, processor)
            new_df_rows_data.append((val, b.name, c))

    # Construct pd.DataFrame with the result of the scalar indicator calculation
    df2 = pd.DataFrame(data=new_df_rows_data,
                       index=pd.MultiIndex.from_tuples(new_df_rows_idx, names=idx_names),
                       columns=["Value", "Benchmark", "Category"])

    return df2


def calculate_global_benchmarks(df_global_indicators, indicators: List[Indicator]):
    """
    From the dataframe of global indicators: scenario, period, indicator, value
    Prepare a dataframe with columns: scenario, period, indicator, benchmark, value

    :param df_local_indicators:
    :param glb_idx:
    :return:
    """
    if df_global_indicators.empty:
        return pd.DataFrame()

    ind_map = create_dictionary()
    for si in indicators:
        if si._indicator_category == IndicatorCategories.case_study:
            if len(si.benchmarks) > 0:
                ind_map[si.name] = si

    idx_names = ["Scenario", "Period"]  # Changing factors

    new_df_rows_idx = []
    new_df_rows_data = []
    indicator_column_idx = df_global_indicators.columns.get_loc("Indicator")
    value_column_idx = df_global_indicators.columns.get_loc("Value")
    unit_column_idx = df_global_indicators.columns.get_loc("Unit")
    for r in df_global_indicators.itertuples():
        indic = r[1+indicator_column_idx]
        ind = ind_map[indic]
        val = r[1+value_column_idx]
        unit = r[1+unit_column_idx]
        for b in ind.benchmarks:
            c = get_benchmark_category(b, val)
            if not c:
                c = f"<out ({val})>"

            new_df_rows_idx.append(r[0])  # (scenario, period, scope, processor)
            new_df_rows_data.append((indic, val, b.name, c))

    # Construct pd.DataFrame with the result of the scalar indicator calculation
    df2 = pd.DataFrame(data=new_df_rows_data,
                       index=pd.MultiIndex.from_tuples(new_df_rows_idx, names=idx_names),
                       columns=["Indicator", "Value", "Benchmark", "Category"])

    return df2


def prepare_matrix_indicators(indicators: List[MatrixIndicator],
                              registry: PartialRetrievalDictionary,
                              serialized_model: lxml.etree._ElementTree, p_map: Dict,
                              interface_results: pd.DataFrame, indicator_results: pd.DataFrame,
                              dynamic_scenario: bool) -> Dict[str, Dataset]:
    """
    Compute Matrix Indicators

    :param indicators:
    :param registry:
    :param serialized_model:
    :param p_map:
    :param interface_results: The pd.DataFrame with all the interface results
    :param indicator_results: The pd.DataFrame with all the local scalar indicators
    :param dynamic_scenario: True if the matrices have to be prepared for a dynamic scenario
    :return: A dictionary <dataset_name> -> <dataset>
    """

    def prepare_matrix_indicator(indicator: MatrixIndicator) -> pd.DataFrame:
        """
        Compute a Matrix Indicator

        :param indicator: the MatrixIndicator to consider
        :param serialized_model: model as result of parsing XML serialization of model (Processors and Interfaces; no relationships nor observations)
        :param results: result of graph solver
        :return: a pd.DataFrame containing the desired matrix indicator
        """
        # Filter "Scope", if defined
        indicators_df = indicator_results
        if indicator.scope:
            # TODO Consider case sensitiveness of "indicator.scope" (it is entered by the user)
            interfaces_df = interface_results.query('Scope in ("' + indicator.scope + '")')
            if not indicator_results.empty:
                indicators_df = indicator_results.query(f'Scope in ("{indicator.scope}")')
        else:
            interfaces_df = interface_results

        # Apply XPath to obtain the dataframe filtered by the desired set of processors
        dfs, selected_processors = obtain_subset_of_processors(indicator.processors_selector, serialized_model, registry, p_map, [interfaces_df, indicators_df])
        interfaces_df, indicators_df = dfs[0], dfs[1]

        # Filter Interfaces
        if indicator.interfaces_selector:
            ifaces = set([_.strip() for _ in indicator.interfaces_selector.split(",")])
            if not case_sensitive:
                ifaces = set([_.lower() for _ in ifaces])

            i_names = get_adapted_case_dataframe_filter(interface_results, "Interface", ifaces)
            # i_names = results.index.unique(level="Interface").values
            # i_names_case = [_ if case_sensitive else _.lower() for _ in i_names]
            # i_names_corr = dict(zip(i_names_case, i_names))
            # i_names = [i_names_corr[_] for _ in ifaces]
            # Filter dataframe to only the desired Interfaces.
            interfaces_df = interfaces_df.query('Interface in [' + ', '.join(['"' + _ + '"' for _ in i_names]) + ']')

        # Filter ScalarIndicators
        if indicator.indicators_selector:
            inds = set([_.strip() for _ in indicator.indicators_selector.split(",")])
            if not case_sensitive:
                inds = set([_.lower() for _ in inds])

            i_names = get_adapted_case_dataframe_filter(indicator_results, "Indicator", inds)
            indicators_df = indicators_df.query('Indicator in [' + ', '.join(['"' + _ + '"' for _ in i_names]) + ']')

        # Filter Attributes
        if indicator.attributes_selector:
            attribs = set([_.strip() for _ in indicator.attributes_selector.split(",")])
            if not case_sensitive:
                attribs = set([_.lower() for _ in attribs])

            # Attributes
            i_names = get_adapted_case_dataframe_filter(interface_results, "Interface", attribs)
            attributes_df = interfaces_df.query('Interface in [' + ', '.join(['"' + _ + '"' for _ in i_names]) + ']')

        # Pivot Table: Dimensions (rows) are (Scenario, Period, Processor[, Scope])
        #              Dimensions (columns) are (Interface, Orientation -of Interface-)
        #              Measures (cells) are (Value)
        idx_columns = ["Scenario", "Period", "Processor"]
        if indicator.scope:
            idx_columns.append("Scope")
        interfaces_df = interfaces_df.pivot_table(values="Value", index=idx_columns, columns=["Interface", "Orientation"])
        # Flatten columns, concatenating levels
        interfaces_df.columns = [f"{x} {y}" for x, y in zip(interfaces_df.columns.get_level_values(0), interfaces_df.columns.get_level_values(1))]

        if not indicators_df.empty:
            indicators_df = indicators_df.pivot_table(values="Value", index=idx_columns, columns=["Indicator"])
            interfaces_df = pd.merge(interfaces_df, indicators_df, how="outer", left_index=True, right_index=True)

        return interfaces_df

    # For each MatrixIndicator...
    result = {}
    for mi in indicators:
        df = prepare_matrix_indicator(mi)
        ds_name = mi.name
        if dynamic_scenario:
            ds_name = "dyn_"+ds_name
        ds = get_dataset(df, ds_name, mi.description)
        result[ds_name] = ds

    return result


def get_eum_dataset(dataframe: pd.DataFrame) -> "Dataset":
    # EUM columns
    df = dataframe.query('Orientation == "Input" and '
                         'Interface in ["Biofuel", "CropProduction", "Fertilizer", "HA", "LU"]')

    # EUM rows
    df = df.query(
        'Processor in ['
        '"Society", "Society.Biodiesel", "Society.Bioethanol", '
        '"Society.CommerceImports", "Society.CommerceExports", '
        '"Society.Bioethanol.Cereals", '
        '"Society.Bioethanol.Cereals.Wheat", "Society.Bioethanol.Cereals.Maize", '
        '"Society.Bioethanol.Cereals.ExternalWheat", "Society.Bioethanol.Cereals.ExternalMaize", '
        '"Society.Bioethanol.SugarCrops", '
        '"Society.Bioethanol.SugarCrops.SugarBeet", "Society.Bioethanol.SugarCrops.SugarCane", '
        '"Society.Bioethanol.SugarCrops.ExternalSugarBeet", "Society.Bioethanol.SugarCrops.ExternalSugarCane", '
        '"Society.Biodiesel.OilCrops", '
        '"Society.Biodiesel.OilCrops.PalmOil", "Society.Biodiesel.OilCrops.RapeSeed", '
        '"Society.Biodiesel.OilCrops.SoyBean", '
        '"Society.Biodiesel.OilCrops.ExternalPalmOil", "Society.Biodiesel.OilCrops.ExternalRapeSeed", '
        '"Society.Biodiesel.OilCrops.ExternalSoyBean"'
        ']'
    )

    df = df.pivot_table(values="Value", index=["Scenario", "Period", "Processor", "Level"], columns="Interface")

    # Adding units to column name
    # TODO: remove hardcoded
    df = df.rename(columns={"Biofuel": "Biofuel (tonnes)",
                            "CropProduction": "CropProduction (tonnes)",
                            "Fertilizer": "Fertilizer (kg)",
                            "HA": "HA (h)",
                            "LU": "LU (ha)"})

    print(df)

    return get_dataset(df, "end_use_matrix", "End use matrix")


def get_dataset(dataframe: pd.DataFrame, code: str, description: str) -> "Dataset":
    ds = Dataset()
    ds.data = dataframe.reset_index()
    ds.code = code
    ds.description = description
    ds.attributes = {}
    ds.metadata = None
    ds.database = None

    if dataframe.index.names[0] != None:
        for dimension in dataframe.index.names:  # type: str
            d = Dimension()
            d.code = dimension
            d.description = None
            d.attributes = None
            d.is_time = (dimension.lower() == "period")
            d.is_measure = False
            cl = dataframe.index.unique(level=dimension).values
            d.code_list = CodeList.construct(
                dimension, dimension, [""],
                codes=[CodeImmutable(c, c, "", []) for c in cl]
            )
            d.dataset = ds

    for measure in dataframe.columns.values:  # type: str
        d = Dimension()
        d.code = measure
        d.description = None
        d.attributes = None
        d.is_time = False
        d.is_measure = True
        d.dataset = ds

    return ds
