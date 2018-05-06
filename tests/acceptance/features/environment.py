import os

import botocore.session

SESSION = botocore.session.get_session()
KNOWN_SERVICES = SESSION.get_available_services()

# For the services where the tag name doesn't match
# the name we use to create_client(), we need to maintain
# a map until we can get these changes pushed upstream.
TAG_TO_ENDPOINT_PREFIX = {
    'cognitoidentity': 'cognito-identity',
    'cognitosync': 'cognito-sync',
    'elasticloadbalancing': 'elb',
    'elasticfilesystem': 'efs',
}
REGION = 'us-east-1'
REGION_OVERRIDES = {
    'devicefarm': 'us-west-2',
    'efs': 'us-west-2',
}
SKIP_SERVICES = set([
    # efs/support require subscriptions and may not work on every machine.
    'efs',
    'support',
    # sts and importexport are skipped because they do not
    # work when using temporary credentials.
    'sts',
    'importexport',
])


def before_feature(context, feature):
    for tag in feature.tags:
        if tag in TAG_TO_ENDPOINT_PREFIX:
            service_name = TAG_TO_ENDPOINT_PREFIX[tag]
            break
        elif tag in KNOWN_SERVICES:
            service_name = tag
            break
    else:
        raise RuntimeError("Unable to create a client for "
                           "feature: %s" % feature)

    if service_name in SKIP_SERVICES:
        feature.mark_skipped()
        return
    region_name = _get_region_for_service(service_name)
    context.client = SESSION.create_client(service_name, region_name)


def _get_region_for_service(service_name):
    if os.environ.get('AWS_SMOKE_TEST_REGION', ''):
        region_name = os.environ['AWS_SMOKE_TEST_REGION']
    else:
        region_name = REGION_OVERRIDES.get(service_name, REGION)
    return region_name
