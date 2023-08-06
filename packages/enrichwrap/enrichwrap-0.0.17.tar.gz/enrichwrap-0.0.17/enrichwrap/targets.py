import logging

enrich_targets = {}


def setup_default_enrich_targets():
    global enrich_targets
    enrich_targets = {
        'socure': {
            'url': 'http://localhost:8100/socure/items',
            'body': {
                'modules': [
                    'fraud', 'phonerisk', 'addressrisk', 'emailrisk', 'kyc', 'social', 'watchliststandard', 'alertlist'
                ],
                'firstName': '',
                'surName': '',
                'email': '',
                'dob': '',
                'physicalAddress': '',
                'physicalAddress2': '',
                'city': '',
                'state': '',
                'country': '',
                'zip': '',
                'mobileNumber': '',
                'nationalId': '',
                'driverLicense': '',
                'driverLicenseState': '',
            },
            'mechanism': 'POST'
        },
        # TODO - need to check on payfone site for details if different than ID360/boss
        'payfonetrust': {
            'url': 'http://localhost:8100/payfone/trust/v2',
            'body': {
                'requestId': '',
                'details': '',
                'consentStatus': '',
                'phoneNumber': '',
            },
            'mechanism': 'POST'
        },
        'payfoneverify': {
            'url': 'http://localhost:8100/payfone/identity/verify/v2',
            'body': {
                'requestId': '',
                'payfoneAlias': '',
                'firstName': '',
                'lastName': '',
                'address': '',
                'extendedAddress': '',
                'city': '',
                'region': '',
                'postalCode': '',
                'lastVerified': '',
                'details': False,
                'phoneUpdate': False,
            },
            'mechanism': 'POST'
        },
        'threatmetrix': {
            'url': 'http://localhost:8100/threadmetrix',
            'params': [],
            'mechanism': 'GET'
        },
        #    'giact': 'http://localhost:8100/giact/items',
        'biocatch': {
            'url': 'http://localhost:8100/biocatch/items',
            'params': [],
            'mechanism': 'GET'
        },
        'bokugpir': {
            # getPhoneIdentificationResult
            'url': 'http://localhost:8100/boku/retrieve-evurl/items',
            'body': {
                'merchantId':'',
                'correlationId': '',
                'associationKey': '',
                'match': {
                    'consumerMdn': ''
                }
            },
            'mechanism': 'POST'
        },
        'bokumaa': {
            'url': 'http://localhost:8100/boku/match/items',
            'body': {
                'merchantId': '',
                'subMerchantId': '',
                'consentId': '',
                'consentTimeStamp': '',
                'msisdn': '',
                'correlationId': '',
                'firstName': '',
                'lastName': '',
                'address1': '',
                'address2': '',
                'city': '',
                'state': '',
                'postalCode': '',
                'countryCode': '',
                'nationalId': '',
                'dateOfBirth': ''
            },
            'mechanism': 'POST'
        }
    }

    return enrich_targets


def Update_enrich_target(which_enrich, map_new_data):
    # Validate that I have what I need
    if 'url' not in map_new_data.keys() or 'mechanism' not in map_new_data.keys():
        logging.error('MISSING values in updating enrich target - ignoring.  Need "url" and "mechanism" at the least [%s]'%map_new_data)
        return
    mechanism = map_new_data.get('mechanism')
    if mechanism.lower() == 'post' and 'body' not in map_new_data.keys():
        logging.error('If POST is the mechanism, then body must be provided [%s]' %map_new_data)
        return
    elif mechanism.lower() == 'get' and 'params' not in map_new_data.keys():
        logging.error('If GET is the mechanism, then params must be provided [%s]' %map_new_data)
        return

    enrich_targets[which_enrich] = map_new_data


def Get_enrich_target(which_enrich):
    return enrich_targets[which_enrich]


def set_enrich_targets(map):
    global enrich_targets
    enrich_targets = map
    return enrich_targets
