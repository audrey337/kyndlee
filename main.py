import os
import sys
import json
from fuzzywuzzy import fuzz

from gepir import GEPIR
from gepir.elements import GetKeyLicenseeResponse, GetPrefixLicenseeResponse, GetPartyByNameResponse, GEPIRParty, PartyDataLine, GEPIRItem, ItemDataLine


def get_party_name(gtin): 
    gepir = GEPIR(
        requester_gln='0000000000000'
    )
    
    gklr = gepir.get_key_licensee(
        requested_key_code='GTIN',
        requested_key_value=gtin
    ) # type: GetKeyLicenseeResponse
    return gklr.gepir_party[0].party_data_line[0].gs1_company_prefix_licensee.party_name[0]
    
def search_list(list_type, q):
    with open(f"{list_type}.json",'r') as json_file:
        data = json.load(json_file)
    return max(fuzz.ratio(q.lower(), row) for row in data)


if __name__ == "__main__":
    party_name = get_party_name(sys.argv[1])
    dont_match = search_list("companiesdonttest", party_name)
    do_match = search_list("companiesdotest", party_name)
    print(f"company={party_name} dont={dont_match} do={do_match}")
