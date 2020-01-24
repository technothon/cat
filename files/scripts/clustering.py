#!/usr/bin/env python

from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import AffinityPropagation
from collections import OrderedDict, defaultdict
import numpy
import scipy.stats as stats
import pandas as pd
import os.path
import csv
import json
#import matplotlib.pyplot as plt
from itertools import cycle

replaceStringDict = {
         "a-only": 1.0,
         "a-srv-naptr" : 2.0,
         "allow": 1.0,
         "both": 1.0,
         "convert": 0.0,
         "default": 0.0,
         "disabled": 0.0,
         "dryUp": 1.0,
         "enabled": 1.0,
         "exclude": 0.0,
         "lastProvResponse": 1.0,
         "localignored": 0.0,
         "noAction": 0.0,
         "none": 0.0,
         "outOfService": 0.0,
         "passthru": 1.0,
         "required": 1.0,
         "supported": 1.0,
         "synchronous": 0.0,
         "treatAsFaxTransmissionIndication": 1,
         "unlimited": 100.0,
         "inService": 1.0,
         "passive": 0.0,
         "matchSigAddrType": 0.0,
         "firstProvResponse": 2.0,
         "force": 1.0,
         "challengeForRegister": 1.0,
         "unlimited": 100.0,
         "noValidation": 0.0,
         "release": 1.0
    }
columnNamesDict = {
         "a-only": ["services_dnsSupportType"],
         "a-srv-naptr": ["services_dnsSupportType"],
         "allow": ["signaling_methods_message","signaling_methods_notify","signaling_methods_publish","signaling_methods_options","signaling_methods_subscribe","signaling_methods_update","signaling_methods_register"],
         "both": ["signaling_timers_suspendResumeTimer_type","signaling_timers_suspendResumeTimer_type"],
         "convert": ["media_lateMediaSupport","media_lateMediaSupport"],
         "default": ["signaling_privacyParamRestricted"],
         "disabled": ["maskPortforRcb","enforceAORMatch","maskIpAddressforRcb","state","mode","action","recorder","siprec","authentication_intChallengeResponse","surrogateRegistration_state","authentication_incInternalCredentials","pathCheck_statusUpdateSupport","surrogateRegistration_useNextSurrRegForCall","surrogateRegistration_useUserNameAsPAI","pathCheck_state","media_msrp","signaling_isupMimeBodyRelay","callRouting_sendRouteUriToPsx","downstreamForkingSupport","signaling_authentication_intChallengeResponse","signaling_sendSdpToPsx","services_overlapAddressing_receive","congestionHandling_egressThrottling","services_dnsNaptrAlways","signaling_localNumberSupport","signaling_deRegParentWithChildDereg","signaling_rel100Support","signaling_cpcInterworkingForNNI","signaling_acceptHistoryInfo","signaling_strictParse","signaling_storeICID","processSGConfigWhenTGOOS","media_dataPathModePassthru","media_recordable","signaling_usePcfaCcf","signaling_usePSXRouteAsReqUriInReg","services_preconditionIntwkUsing183","signaling_registration_alwaysRandomIntExpires","signaling_useRandomUserInfoInContactHdr","signaling_registration_includeXOriginalAddr","signaling_callingParty_trustedSourceForIsup","signaling_aiToPemInterworking","media_pcrf_cushionPacketSize","signaling_registration_useRUriForRegisterRouting","signaling_callingParty_mapFromHeaderToIsupGAP","signaling_condIncMethInAllowHdr","media_pcrf_terminateOnNwFailure","media_earlyMedia_egressSupport","signaling_validateAor","signaling_relayReplacesHeader","state","services_jsrcBandwidthReservation","media_pcrf_provSignalingFlow","signaling_sourceAddressValidation","services_natTraversal_learnNatForRtpOnly ","services_overlapAddressing_overlapState ","services_natTraversal_iceSourceAddressFilterPriority_state ","signaling_honorMaddrParam","signaling_keepSupport ","signaling_support199OptionTag ","callReservation_state ","media_advertiseAudioOnly ","media_pcrf_pcrfSendAarOnlyForSessionAnswer","media_directMediaAllowedBehindNapt","services_natTraversal_signalingNat","signaling_usePortRangeFlag","signaling_callingParty_mapIsupCgpnToPAI","media_omrAllowed","signaling_dnsForceReQuery","signaling_enforceSipsIfEgressIsTls","signaling_usePsxRouteForEmergencyCall","signaling_rfc3261ValidateInvite200OkRetransmissions","services_remoteEPreservation","signaling_callingParty_fromHdrForCallingParty","signaling_outboundSupport","media_tmr64K","signaling_treatPortZeroAsNoAudio","signaling_skipDTGLookupForRouteHdr","signaling_relayUpdatewithSdp","signaling_sdp100relIwkForPrack","signaling_timers_suspendResumeTimer_state","signaling_sdpTransparency_sdpTransparencyState","media_lyncShare","media_directMediaAntiTrombone","signaling_relayNonInviteRequest","signaling_callingParty_rpiForCallingParty","signaling_causeCodeMapping_useNonDefaultCauseCodeforARSBlackList","signaling_P-HeaderExtensions_useIngressOrigCa","callReservation_silc_state","callRouting_dnsCrankback","packetOutage_detectionState","callRouting_useRouteSet","signaling_rfc3261ValidateCSeqInBYE","media_pcrf_signallingPath","signaling_stopLmsdToneOnUpdate","signaling_registration_alwaysRandomExtExpires","signaling_authentication_incInternalCredentials","services_dialogEventNotificationSupported","media_pcrf_cushionNullSdp","media_directMediaAllowed","services_natTraversal_mediaNat","services_sipJurisdictionSupport","signaling_rewriteIdentities","callRouting_addStoredPathAsTopRoute","services_overlapAddressing_send","signaling_backwardInfoMsgConDialog","services_colocatedPandEcscf","signaling_callingParty_ppiForCallingParty","callRouting_internationalNoaPlus","signaling_prefRequireTransparency","signaling_registration_bulkRegisterFormat","signaling_psxRouteForSubscribe","services_natTraversal_adaptiveLearning_state","signaling_ocsSupport","signaling_messageManipulation_includeAppHdrs","signaling_disableTermIOIForPcscf","media_sdpAttributesSelectiveRelay","signaling_P-HeaderExtensions_addEgressOrigCa"],
         "dryUp": ["action"],
         "enabled": ["maskPortforRcb","enforceAORMatch","maskIpAddressforRcb","state","mode","action","recorder","siprec","authentication_intChallengeResponse","surrogateRegistration_state","authentication_incInternalCredentials","pathCheck_statusUpdateSupport","surrogateRegistration_useNextSurrRegForCall","pathCheck_state","surrogateRegistration_suppressRegRetryAfterAuthFail","surrogateRegistration_useUserNameAsPAI","media_msrp","signaling_isupMimeBodyRelay","callRouting_sendRouteUriToPsx","downstreamForkingSupport","signaling_authentication_intChallengeResponse","signaling_sendSdpToPsx","services_overlapAddressing_receive","congestionHandling_egressThrottling","services_dnsNaptrAlways","signaling_localNumberSupport","signaling_deRegParentWithChildDereg","signaling_rel100Support","signaling_cpcInterworkingForNNI","signaling_acceptHistoryInfo","signaling_strictParse","signaling_storeICID","processSGConfigWhenTGOOS","media_dataPathModePassthru","media_recordable","signaling_usePcfaCcf","signaling_usePSXRouteAsReqUriInReg","services_preconditionIntwkUsing183","signaling_registration_alwaysRandomIntExpires","signaling_useRandomUserInfoInContactHdr","signaling_registration_includeXOriginalAddr","signaling_callingParty_trustedSourceForIsup","signaling_aiToPemInterworking","media_pcrf_cushionPacketSize","signaling_registration_useRUriForRegisterRouting","signaling_callingParty_mapFromHeaderToIsupGAP","signaling_condIncMethInAllowHdr","media_pcrf_terminateOnNwFailure","media_earlyMedia_egressSupport","signaling_validateAor","signaling_relayReplacesHeader","state","services_jsrcBandwidthReservation","media_pcrf_provSignalingFlow","signaling_sourceAddressValidation","services_natTraversal_learnNatForRtpOnly ","services_overlapAddressing_overlapState ","services_natTraversal_iceSourceAddressFilterPriority_state ","signaling_honorMaddrParam","signaling_keepSupport ","signaling_support199OptionTag ","callReservation_state ","media_advertiseAudioOnly ","media_pcrf_pcrfSendAarOnlyForSessionAnswer","media_directMediaAllowedBehindNapt","services_natTraversal_signalingNat","signaling_usePortRangeFlag","signaling_callingParty_mapIsupCgpnToPAI","media_omrAllowed","signaling_dnsForceReQuery","signaling_enforceSipsIfEgressIsTls","signaling_usePsxRouteForEmergencyCall","signaling_rfc3261ValidateInvite200OkRetransmissions","services_remoteEPreservation","signaling_callingParty_fromHdrForCallingParty","signaling_outboundSupport","media_tmr64K","signaling_treatPortZeroAsNoAudio","signaling_skipDTGLookupForRouteHdr","signaling_relayUpdatewithSdp","signaling_sdp100relIwkForPrack","signaling_timers_suspendResumeTimer_state","signaling_sdpTransparency_sdpTransparencyState","media_lyncShare","media_directMediaAntiTrombone","signaling_relayNonInviteRequest","signaling_callingParty_rpiForCallingParty","signaling_causeCodeMapping_useNonDefaultCauseCodeforARSBlackList","signaling_P-HeaderExtensions_useIngressOrigCa","callReservation_silc_state","callRouting_dnsCrankback","packetOutage_detectionState","callRouting_useRouteSet","signaling_rfc3261ValidateCSeqInBYE","media_pcrf_signallingPath","signaling_stopLmsdToneOnUpdate","signaling_registration_alwaysRandomExtExpires","signaling_authentication_incInternalCredentials","services_dialogEventNotificationSupported","media_pcrf_cushionNullSdp","media_directMediaAllowed","services_natTraversal_mediaNat","services_sipJurisdictionSupport","signaling_rewriteIdentities","callRouting_addStoredPathAsTopRoute","services_overlapAddressing_send","signaling_backwardInfoMsgConDialog","services_colocatedPandEcscf","signaling_callingParty_ppiForCallingParty","callRouting_internationalNoaPlus","signaling_prefRequireTransparency","signaling_registration_bulkRegisterFormat","signaling_psxRouteForSubscribe","services_natTraversal_adaptiveLearning_state","signaling_ocsSupport","signaling_messageManipulation_includeAppHdrs","signaling_disableTermIOIForPcscf","media_sdpAttributesSelectiveRelay","signaling_P-HeaderExtensions_addEgressOrigCa"],
         "exclude": ["services_longDurationCall_emergencyOrPriorityCalls","services_longDurationCall_emergencyCalls"],
         "lastProvResponse": ["media_earlyMedia_forkingBehaviour"],
         "localignored": ["tgMtrgResAllocation"],
         "noAction": [],
         "none": ["signaling_accessClass","ucidSupport","media_mediaPortRange_maxUdpPort","signaling_X-Headers_HeaderFlag","services_natTraversal_iceSupport","media_comediaConnectionRole","media_pcrf_pcrfCommitment","services_emergencyCallHandlingMode","media_pcrf_fetchLocationInfo","signaling_transportPreference_preference4","signaling_registration_requireRegistration","media_tcpPortRange_maxServerPort","blockDirection","cac_ingress_otherReqBurstMax","services_preconditions"],
         "outOfService": ["mode"],
         "passthru": [],
         "required": ["signaling_registration_requireRegistration"],
         "supported": ["services_transmitPreconditions"],
         "synchronous": ["media_pcrf_pcrfInteractionMode"],
         "treatAsFaxTransmissionIndication": ["signaling_silenceSuppTreatment"],
         "unlimited": ["ingress_callLimit","callLimit","ingress_callBurstMax","egress_callRateMax","ingress_otherReqRateMax","ingress_callRateMax","egress_registerBurstMax","egress_registerRateMax","egress_subscribeBurstMax","ingress_otherReqBurstMax","egress_otherReqRateMax","ingress_registerRateMax","ingress_subscribeBurstMax","egress_callBurstMax","tcpMediaLimit","registrationLimit","ingress_registerBurstMax","ingress_subscribeRateMax","egress_otherReqBurstMax","egress_callLimit","egress_subscribeRateMax","subscriptionLimit","bandwidthLimit","cac_bandwidthLimit","cac_egress_subscribeRateMax","cac_egress_callBurstMax","cac_ingress_callBurstMax","cac_subscriptionLimit","cac_egress_registerRateMax","cac_ingress_callLimit","cac_registrationLimit"],
         "inService": ["mode"],
         "passive": ["services_natTraversal_iceTcpRole"],
         "matchSigAddrType": ["media_mediaAddrType"],
         "firstProvResponse": ["media_earlyMedia_forkingBehaviour"],
         "force": [],
         "challengeForRegister": [],
         "unlimited": ["ingress_callLimit","callLimit","ingress_callBurstMax","egress_callRateMax","ingress_otherReqRateMax","ingress_callRateMax","egress_registerBurstMax","egress_registerRateMax","egress_subscribeBurstMax","ingress_otherReqBurstMax","egress_otherReqRateMax","ingress_registerRateMax","ingress_subscribeBurstMax","egress_callBurstMax","tcpMediaLimit","registrationLimit","ingress_registerBurstMax","ingress_subscribeRateMax","egress_otherReqBurstMax","egress_callLimit","egress_subscribeRateMax","subscriptionLimit","bandwidthLimit","cac_ingress_registerBurstMax","cac_ingress_otherReqRateMax","cac_ingress_callRateMax","cac_egress_otherReqBurstMax","cac_ingress_subscribeRateMax","cac_callLimit","cac_egress_callLimit","tgMtrgReqMaxBw","cac_egress_otherReqRateMax","cac_ingress_registerRateMax","cac_egress_registerBurstMax","cac_egress_subscribeBurstMax","cac_egress_callRateMax","tgMtrgReqMaxCalls"],
         "noValidation": ["signaling_routeMsgValidation"],
         "release": ["callRouting_ansSupervisionTimeoutAction"]
}

# clustering algorithm
def cluster_fun(file_path):
    df = pd.read_csv (file_path)
    X = df.iloc[:,:]
    X.fillna(X.mean(), inplace=True)
    af = DBSCAN(eps=3, min_samples=10).fit(X)
    labels = af.labels_
    #af = AffinityPropagation(preference=-50)
    #af.fit(X)
    #cluster_centers_indices = af.cluster_centers_indices_
    #labels = af.labels_
    cluster = defaultdict(list)
    for index in range(len(labels)):
        cluster[str(labels[index])].append(str(index))
    return cluster, df

# read input csv based on the cluster values
def post_process(cluster, file_path):
    df = pd.read_csv (file_path)
    conf_dict = {}
    for val in cluster:
        row_num = cluster[val][0]
        row_data = df.iloc[[row_num]]
        for replaceVal, columnList in columnNamesDict.items():
            findVal = replaceStringDict[replaceVal]
            for col in columnList:
                if col in row_data:
                    row_data[col] = row_data[col].replace(findVal, replaceVal)
        conf_dict[val] = (row_data.to_dict(orient='index'))
    return conf_dict
                    
    
#check if file exists in the given path then pass one by one file to the clustering algorithm
def main():
    #read the the configuration
    conf_list = ['sipSigPort','ipPeer','sipTrunkGroup','cac']
    for i in conf_list:
        input_path = os.path.join('C:\\Users\\sbalakatti\\Desktop\\Technothon', i+".csv")
        output_path = os.path.join('C:\\Users\\sbalakatti\\Desktop\\Technothon', i+".json")
        if os.path.exists(input_path):
            cluster, df=cluster_fun(input_path)  
            cluster=dict(cluster)
            conf_dict=post_process(cluster, input_path)
            if os.path.exists(output_path):
                mode = 'w'
            else:
                mode = 'a'
            json_data=json.dumps(cluster)
            with open(output_path,mode) as file:
                file.write(json_data)
       
main()

    
