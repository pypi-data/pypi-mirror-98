"""
Various webhook configurations
"""

from typing import List, Optional

from avionix.kube.apiextensions import WebhookClientConfig
from avionix.kube.base_objects import AdmissionRegistration
from avionix.kube.meta import LabelSelector, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class RuleWithOperations(HelmYaml):
    """
    :param api_groups: APIGroups is the API groups the resources belong to. '\\*' is \
        all groups. If '\\*' is present, the length of the slice must be one. \
        Required.
    :param api_versions: APIVersions is the API versions the resources belong to. '\\*' \
        is all versions. If '\\*' is present, the length of the slice must be one. \
        Required.
    :param operations: Operations is the operations the admission hook cares about - \
        CREATE, UPDATE, or * for all operations. If '\\*' is present, the length of \
        the slice must be one. Required.
    :param resources: Resources is a list of resources this rule applies to.  For \
        example: 'pods' means pods. 'pods/log' means the log subresource of pods. \
        '\\*' means all resources, but not subresources. 'pods/\\*' means all \
        subresources of pods. '\\*/scale' means all scale subresources. '\\*/\\*' \
        means all resources and their subresources.  If wildcard is present, the \
        validation rule will ensure resources do not overlap with each other.  \
        Depending on the enclosing object, subresources might not be allowed. \
        Required.
    :param scope: scope specifies the scope of this rule. Valid values are "Cluster", \
        "Namespaced", and "*" "Cluster" means that only cluster-scoped resources will \
        match this rule. Namespace API objects are cluster-scoped. "Namespaced" means \
        that only namespaced resources will match this rule. "*" means that there are \
        no scope restrictions. Subresources match the scope of their parent resource. \
        Default is "*".
    """

    def __init__(
        self,
        api_groups: List[str],
        api_versions: List[str],
        operations: List[str],
        resources: List[str],
        scope: Optional[str] = None,
    ):
        self.apiGroups = api_groups
        self.apiVersions = api_versions
        self.operations = operations
        self.resources = resources
        self.scope = scope


class ValidatingWebhook(HelmYaml):
    """
    :param name: The name of the admission webhook. Name should be fully qualified, \
        e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of the \
        webhook, and kubernetes.io is the name of the organization. Required.
    :param admission_review_versions: AdmissionReviewVersions is an ordered list of \
        preferred `AdmissionReview` versions the Webhook expects. API server will try \
        to use first version in the list which it supports. If none of the versions \
        specified in this list supported by API server, validation will fail for this \
        object. If a persisted webhook configuration specifies allowed versions and \
        does not include any versions known to the API Server, calls to the webhook \
        will fail and be subject to the failure policy.
    :param client_config: ClientConfig defines how to communicate with the hook. \
        Required
    :param side_effects: SideEffects states whether this webhook has side effects. \
        Acceptable values are: None, NoneOnDryRun (webhooks created via v1beta1 may \
        also specify Some or Unknown). Webhooks with side effects MUST implement a \
        reconciliation system, since a request may be rejected by a future step in the \
        admission change and the side effects therefore need to be undone. Requests \
        with the dryRun attribute will be auto-rejected if they match a webhook with \
        sideEffects == Unknown or Some.
    :param failure_policy: FailurePolicy defines how unrecognized errors from the \
        admission endpoint are handled - allowed values are Ignore or Fail. Defaults \
        to Fail.
    :param match_policy: matchPolicy defines how the "rules" list is used to match \
        incoming requests. Allowed values are "Exact" or "Equivalent".  - Exact: match \
        a request only if it exactly matches a specified rule. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        but "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would not be \
        sent to the webhook.  - Equivalent: match a request if modifies a resource \
        listed in rules, even via another API group or version. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        and "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would be \
        converted to apps/v1 and sent to the webhook.  Defaults to "Equivalent"
    :param namespace_selector: NamespaceSelector decides whether to run the webhook on \
        an object based on whether the namespace for that object matches the selector. \
        If the object itself is a namespace, the matching is performed on \
        object.metadata.labels. If the object is another cluster scoped resource, it \
        never skips the webhook.  For example, to run the webhook on any objects whose \
        namespace is not associated with "runlevel" of "0" or "1";  you will set the \
        selector as follows: "namespaceSelector": {   "matchExpressions": [     {      \
         "key": "runlevel",       "operator": "NotIn",       "values": [         "0",  \
               "1"       ]     }   ] }  If instead you want to only run the webhook on \
        any objects whose namespace is associated with the "environment" of "prod" or \
        "staging"; you will set the selector as follows: "namespaceSelector": {   \
        "matchExpressions": [     {       "key": "environment",       "operator": \
        "In",       "values": [         "prod",         "staging"       ]     }   ] }  \
        See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels \
        for more examples of label selectors.  Default to the empty LabelSelector, \
        which matches everything.
    :param object_selector: ObjectSelector decides whether to run the webhook based on \
        if the object has matching labels. objectSelector is evaluated against both \
        the oldObject and newObject that would be sent to the webhook, and is \
        considered to match if either object matches the selector. A null object \
        (oldObject in the case of create, or newObject in the case of delete) or an \
        object that cannot have labels (like a DeploymentRollback or a PodProxyOptions \
        object) is not considered to match. Use the object selector only if the \
        webhook is opt-in, because end users may skip the admission webhook by setting \
        the labels. Default to the empty LabelSelector, which matches everything.
    :param rules: Rules describes what operations on what resources/subresources the \
        webhook cares about. The webhook cares about an operation if it matches _any_ \
        Rule. However, in order to prevent ValidatingAdmissionWebhooks and \
        MutatingAdmissionWebhooks from putting the cluster in a state which cannot be \
        recovered from without completely disabling the plugin, \
        ValidatingAdmissionWebhooks and MutatingAdmissionWebhooks are never called on \
        admission requests for ValidatingWebhookConfiguration and \
        MutatingWebhookConfiguration objects.
    :param timeout_seconds: TimeoutSeconds specifies the timeout for this webhook. \
        After the timeout passes, the webhook call will be ignored or the API call \
        will fail based on the failure policy. The timeout value must be between 1 and \
        30 seconds. Default to 10 seconds.
    """

    def __init__(
        self,
        name: str,
        admission_review_versions: List[str],
        client_config: WebhookClientConfig,
        side_effects: str,
        failure_policy: Optional[str] = None,
        match_policy: Optional[str] = None,
        namespace_selector: Optional[LabelSelector] = None,
        object_selector: Optional[LabelSelector] = None,
        rules: Optional[List[RuleWithOperations]] = None,
        timeout_seconds: Optional[int] = None,
    ):
        self.name = name
        self.admissionReviewVersions = admission_review_versions
        self.clientConfig = client_config
        self.sideEffects = side_effects
        self.failurePolicy = failure_policy
        self.matchPolicy = match_policy
        self.namespaceSelector = namespace_selector
        self.objectSelector = object_selector
        self.rules = rules
        self.timeoutSeconds = timeout_seconds


class ValidatingWebhookConfiguration(AdmissionRegistration):
    """
    :param metadata: Standard object metadata; More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.  # noqa
    :param webhooks: Webhooks is a list of webhooks and the affected resources and \
        operations.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        webhooks: List[ValidatingWebhook],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.webhooks = webhooks


class MutatingWebhook(HelmYaml):
    """
    :param name: The name of the admission webhook. Name should be fully qualified, \
        e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of the \
        webhook, and kubernetes.io is the name of the organization. Required.
    :param admission_review_versions: AdmissionReviewVersions is an ordered list of \
        preferred `AdmissionReview` versions the Webhook expects. API server will try \
        to use first version in the list which it supports. If none of the versions \
        specified in this list supported by API server, validation will fail for this \
        object. If a persisted webhook configuration specifies allowed versions and \
        does not include any versions known to the API Server, calls to the webhook \
        will fail and be subject to the failure policy.
    :param client_config: ClientConfig defines how to communicate with the hook. \
        Required
    :param side_effects: SideEffects states whether this webhook has side effects. \
        Acceptable values are: None, NoneOnDryRun (webhooks created via v1beta1 may \
        also specify Some or Unknown). Webhooks with side effects MUST implement a \
        reconciliation system, since a request may be rejected by a future step in the \
        admission change and the side effects therefore need to be undone. Requests \
        with the dryRun attribute will be auto-rejected if they match a webhook with \
        sideEffects == Unknown or Some.
    :param failure_policy: FailurePolicy defines how unrecognized errors from the \
        admission endpoint are handled - allowed values are Ignore or Fail. Defaults \
        to Fail.
    :param match_policy: matchPolicy defines how the "rules" list is used to match \
        incoming requests. Allowed values are "Exact" or "Equivalent".  - Exact: match \
        a request only if it exactly matches a specified rule. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        but "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would not be \
        sent to the webhook.  - Equivalent: match a request if modifies a resource \
        listed in rules, even via another API group or version. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        and "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would be \
        converted to apps/v1 and sent to the webhook.  Defaults to "Equivalent"
    :param namespace_selector: NamespaceSelector decides whether to run the webhook on \
        an object based on whether the namespace for that object matches the selector. \
        If the object itself is a namespace, the matching is performed on \
        object.metadata.labels. If the object is another cluster scoped resource, it \
        never skips the webhook.  For example, to run the webhook on any objects whose \
        namespace is not associated with "runlevel" of "0" or "1";  you will set the \
        selector as follows: "namespaceSelector": {   "matchExpressions": [     {      \
         "key": "runlevel",       "operator": "NotIn",       "values": [         "0",  \
               "1"       ]     }   ] }  If instead you want to only run the webhook on \
        any objects whose namespace is associated with the "environment" of "prod" or \
        "staging"; you will set the selector as follows: "namespaceSelector": {   \
        "matchExpressions": [     {       "key": "environment",       "operator": \
        "In",       "values": [         "prod",         "staging"       ]     }   ] }  \
        See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ \
        for more examples of label selectors.  Default to the empty LabelSelector, \
        which matches everything.
    :param object_selector: ObjectSelector decides whether to run the webhook based on \
        if the object has matching labels. objectSelector is evaluated against both \
        the oldObject and newObject that would be sent to the webhook, and is \
        considered to match if either object matches the selector. A null object \
        (oldObject in the case of create, or newObject in the case of delete) or an \
        object that cannot have labels (like a DeploymentRollback or a PodProxyOptions \
        object) is not considered to match. Use the object selector only if the \
        webhook is opt-in, because end users may skip the admission webhook by setting \
        the labels. Default to the empty LabelSelector, which matches everything.
    :param reinvocation_policy: reinvocationPolicy indicates whether this webhook \
        should be called multiple times as part of a single admission evaluation. \
        Allowed values are "Never" and "IfNeeded".  Never: the webhook will not be \
        called more than once in a single admission evaluation.  IfNeeded: the webhook \
        will be called at least one additional time as part of the admission \
        evaluation if the object being admitted is modified by other admission plugins \
        after the initial webhook call. Webhooks that specify this option *must* be \
        idempotent, able to process objects they previously admitted. Note: * the \
        number of additional invocations is not guaranteed to be exactly one. * if \
        additional invocations result in further modifications to the object, webhooks \
        are not guaranteed to be invoked again. * webhooks that use this option may be \
        reordered to minimize the number of additional invocations. * to validate an \
        object after all mutations are guaranteed complete, use a validating admission \
        webhook instead.  Defaults to "Never".
    :param rules: Rules describes what operations on what resources/subresources the \
        webhook cares about. The webhook cares about an operation if it matches _any_ \
        Rule. However, in order to prevent ValidatingAdmissionWebhooks and \
        MutatingAdmissionWebhooks from putting the cluster in a state which cannot be \
        recovered from without completely disabling the plugin, \
        ValidatingAdmissionWebhooks and MutatingAdmissionWebhooks are never called on \
        admission requests for ValidatingWebhookConfiguration and \
        MutatingWebhookConfiguration objects.
    :param timeout_seconds: TimeoutSeconds specifies the timeout for this webhook. \
        After the timeout passes, the webhook call will be ignored or the API call \
        will fail based on the failure policy. The timeout value must be between 1 and \
        30 seconds. Default to 10 seconds.
    """

    def __init__(
        self,
        name: str,
        admission_review_versions: List[str],
        client_config: WebhookClientConfig,
        side_effects: str,
        failure_policy: Optional[str] = None,
        match_policy: Optional[str] = None,
        namespace_selector: Optional[LabelSelector] = None,
        object_selector: Optional[LabelSelector] = None,
        reinvocation_policy: Optional[str] = None,
        rules: Optional[List[RuleWithOperations]] = None,
        timeout_seconds: Optional[int] = None,
    ):
        self.name = name
        self.admissionReviewVersions = admission_review_versions
        self.clientConfig = client_config
        self.sideEffects = side_effects
        self.failurePolicy = failure_policy
        self.matchPolicy = match_policy
        self.namespaceSelector = namespace_selector
        self.objectSelector = object_selector
        self.reinvocationPolicy = reinvocation_policy
        self.rules = rules
        self.timeoutSeconds = timeout_seconds


class MutatingWebhookConfiguration(AdmissionRegistration):
    """
    :param metadata: Standard object metadata; More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.  # noqa
    :param webhooks: Webhooks is a list of webhooks and the affected resources and \
        operations.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        webhooks: List[MutatingWebhook],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.webhooks = webhooks
