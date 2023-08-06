

def default_model_classes():
  from kama_sdk.model.adapters.deletion_spec import DeletionSpec
  from kama_sdk.model.variable.manifest_variable import ManifestVariable
  from kama_sdk.model.input.generic_input import GenericInput
  from kama_sdk.model.input.slider_input import SliderInput
  from kama_sdk.model.adapters.list_resources_adapter import ResourceQueryAdapter
  from kama_sdk.model.operation.operation import Operation
  from kama_sdk.model.adapters.injection_orchestrator import InjectionOrchestrator
  from kama_sdk.model.operation.stage import Stage
  from kama_sdk.model.operation.step import Step
  from kama_sdk.model.operation.field import Field
  from kama_sdk.model.variable.generic_variable import GenericVariable
  from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
  from kama_sdk.model.operation.operation_run_simulator import OperationRunSimulator
  from kama_sdk.model.action.base.multi_action import MultiAction
  from kama_sdk.model.input.checkboxes_input import CheckboxesInput
  from kama_sdk.model.input.checkboxes_input import CheckboxInput
  from kama_sdk.model.variable.variable_value_decorator import VariableValueDecorator
  from kama_sdk.model.variable.pod_scaling_decorator import FixedReplicasDecorator
  from kama_sdk.model.error.error_handler import ErrorHandler
  from kama_sdk.model.error.error_trigger_selector import ErrorTriggerSelector
  from kama_sdk.model.error.error_diagnosis import ErrorDiagnosis
  from kama_sdk.model.error.diagnosis_actionable import DiagnosisActionable
  from kama_sdk.model.supplier.predicate.multi_predicate import MultiPredicate
  from kama_sdk.model.adapters.app_status_computer import AppStatusComputer
  from kama_sdk.model.hook.hook import Hook
  from kama_sdk.model.supplier.base.supplier import Supplier
  from kama_sdk.model.supplier.ext.misc.http_data_supplier import HttpDataSupplier
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier
  from kama_sdk.model.input.checkboxes_input import SelectInput
  from kama_sdk.model.input.select_option import InputOption
  from kama_sdk.model.supplier.ext.misc.endpoint_supplier import EndpointSupplier
  from kama_sdk.model.supplier.ext.misc.random_string_supplier import RandomStringSupplier
  from kama_sdk.model.supplier.ext.biz.master_config_supplier import MasterConfigSupplier
  from kama_sdk.model.action.base.action import Action
  from kama_sdk.model.action.ext.update.run_update_hooks_action import RunUpdateHooksAction
  from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
  from kama_sdk.model.glance.endpoint_glance import EndpointGlance
  from kama_sdk.model.glance.predicate_glance import PredicateGlance
  from kama_sdk.model.glance.percentage_glance import PercentageGlance
  from kama_sdk.model.supplier.ext.prometheus.prometheus_scalar_value_supplier import PrometheusScalarSupplier
  from kama_sdk.model.supplier.ext.prometheus.prometheus_time_series_supplier import PrometheusTimeSeriesSupplier
  from kama_sdk.model.glance.time_series_glance import TimeSeriesGlance
  from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer
  from kama_sdk.model.humanizer.cores_humanizer import CoresHumanizer
  from kama_sdk.model.humanizer.bytes_humanizer import BytesHumanizer
  from kama_sdk.model.supplier.base.merge_supplier import MergeSupplier
  from kama_sdk.model.action.ext.manifest.await_outkomes_settled_action import AwaitOutkomesSettledAction
  from kama_sdk.model.action.ext.manifest.await_predicates_settled_action import AwaitPredicatesSettledAction
  from kama_sdk.model.action.ext.manifest.kubectl_apply_action import KubectlApplyAction
  from kama_sdk.model.action.ext.manifest.template_manifest_action import TemplateManifestAction
  from kama_sdk.model.action.ext.update.update_actions import FetchUpdateAction
  from kama_sdk.model.action.ext.update.update_actions import CommitKteaFromUpdateAction
  from kama_sdk.model.adapters.mock_update import MockUpdate
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction

  from kama_sdk.model.action.ext.misc.wait_action import WaitAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourceAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourcesAction
  from kama_sdk.model.action.ext.manifest.kubectl_dry_run_action import KubectlDryRunAction
  from kama_sdk.model.action.ext.misc.create_backup_action import CreateBackupAction
  from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
  from kama_sdk.model.supplier.base.context_supplier import ContextSupplier
  from kama_sdk.model.supplier.base.switch import Switch
  from kama_sdk.model.action.ext.update.fetch_latest_injection_action import FetchLatestInjectionsAction
  from kama_sdk.model.supplier.predicate.format_predicate import FormatPredicate
  from kama_sdk.model.adapters.system_check import SystemCheck
  from kama_sdk.model.supplier.predicate.common_predicates import TruePredicate
  from kama_sdk.model.supplier.predicate.common_predicates import FalsePredicate
  from kama_sdk.model.supplier.predicate.predicate import Predicate
  from kama_sdk.model.action.ext.manifest.patch_manifest_vars_action import PatchManifestVarsAction
  from kama_sdk.model.action.ext.update.update_actions import LoadVarDefaultsFromKtea
  from kama_sdk.model.action.ext.manifest.patch_manifest_vars_action import WriteManifestVarsAction
  return [
    Operation,
    Stage,
    Step,
    Field,
    Hook,

    GenericVariable,
    ManifestVariable,
    VariableValueDecorator,
    FixedReplicasDecorator,
    ResourceSelector,

    ErrorHandler,
    ErrorTriggerSelector,
    ErrorDiagnosis,
    DiagnosisActionable,

    GenericInput,
    SliderInput,
    SelectInput,
    CheckboxesInput,
    CheckboxInput,
    InputOption,

    Predicate,
    FormatPredicate,
    MultiPredicate,
    TruePredicate,
    FalsePredicate,

    Supplier,
    PropsSupplier,
    ContextSupplier,
    Switch,
    MergeSupplier,
    HttpDataSupplier,
    ResourcesSupplier,
    RandomStringSupplier,
    MasterConfigSupplier,
    EndpointSupplier,
    PrometheusTimeSeriesSupplier,
    PrometheusScalarSupplier,

    AppStatusComputer,
    SystemCheck,

    Action,
    MultiAction,
    PatchManifestVarsAction,
    RunUpdateHooksAction,
    WriteManifestVarsAction,
    LoadVarDefaultsFromKtea,
    FetchLatestInjectionsAction,
    AwaitOutkomesSettledAction,
    AwaitPredicatesSettledAction,
    KubectlApplyAction,
    TemplateManifestAction,
    FetchUpdateAction,
    CommitKteaFromUpdateAction,
    RunPredicateAction,
    RunPredicatesAction,
    WaitAction,
    DeleteResourceAction,
    DeleteResourcesAction,
    KubectlDryRunAction,
    CreateBackupAction,

    ResourceQueryAdapter,
    DeletionSpec,
    InjectionOrchestrator,

    GlanceDescriptor,
    EndpointGlance,
    PredicateGlance,
    PercentageGlance,
    TimeSeriesGlance,

    QuantityHumanizer,
    BytesHumanizer,
    CoresHumanizer,

    OperationRunSimulator,
    MockUpdate
  ]
