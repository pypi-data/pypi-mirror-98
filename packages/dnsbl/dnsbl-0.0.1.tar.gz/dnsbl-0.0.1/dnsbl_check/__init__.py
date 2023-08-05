from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import dns.resolver

allData = {
    "blacklists" : []
}

dnsbl_list = []

def check(dnszone,ip):
    ptrl = [x for x in ip.split(".")][::-1]
    ptr = f"{ptrl[0]}.{ptrl[1]}.{ptrl[2]}.{ptrl[3]}."
    try:
        result = dns.resolver.resolve(ptr+dnszone, 'A')
        response = str(list(result)[0])
        if response in ['127.0.0.2', '127.0.0.3', '127.0.0.9']:
            bl_type = "SPAM"
        elif response in ['127.0.0.4', '127.0.0.5', '127.0.0.6', '127.0.0.7']:
            bl_type = "EXPLOITS"
        else:
            bl_type = "UNKNOWN"
        return {"ip" : ip , "dnszone" : dnszone , "code" : response , "type" : bl_type}
    except:
        return False

def run(ip):
    bl = []
    with ThreadPoolExecutor(max_workers = 1000) as executor:
        results = executor.map(check, dnsbl_list,len(dnsbl_list)*[ip])
        for res in results:
            if(res != False):
                bl.append(res)
    print(f"scan done for ip {ip}")
    return bl

def batch(ips,bls):
    global dnsbl_list
    dnsbl_list = bls
    with ThreadPoolExecutor(max_workers = 100) as mainexe:
        jobs = mainexe.map(run, ips)
        for job in jobs:
            if(len(job)>0):
                allData["blacklists"].extend(job)
    return allData

# res = batch(["10.10.204.12","10.10.204.13","10.10.204.14"],['all.s5h.net', 'blacklist.woody.ch', 'combined.abuse.ch', 'dnsbl-2.uceprotect.net', 'dnsbl.sorbs.net', 'dul.dnsbl.sorbs.net', 'ips.backscatterer.org', 'misc.dnsbl.sorbs.net', 'pbl.spamhaus.org', 'relays.bl.gweep.ca', 'singular.ttk.pte.hu', 'spam.abuse.ch', 'spam.spamrats.com', 'spamsources.fabel.dk', 'virus.rbl.jp', 'xbl.spamhaus.org', 'zombie.dnsbl.sorbs.net', 'b.barracudacentral.org', 'bogons.cymru.com', 'db.wpbl.info', 'dnsbl-3.uceprotect.net', 'drone.abuse.ch', 'dyna.spamrats.com', 'ix.dnsbl.manitu.net', 'noptr.spamrats.com', 'proxy.bl.gweep.ca', 'relays.nether.net', 'smtp.dnsbl.sorbs.net', 'spam.dnsbl.anonmails.de', 'spambot.bls.digibase.ca', 'ubl.lashback.com', 'web.dnsbl.sorbs.net', 'bl.spamcop.net', 'cbl.abuseat.org', 'dnsbl-1.uceprotect.net', 'dnsbl.dronebl.org', 'duinv.aupads.org', 'http.dnsbl.sorbs.net', 'korea.services.net', 'orvedb.aupads.org', 'psbl.surriel.com', 'sbl.spamhaus.org', 'socks.dnsbl.sorbs.net', 'spam.dnsbl.sorbs.net', 'spamrbl.imp.ch', 'ubl.unsubscore.com', 'wormrbl.imp.ch', 'zen.spamhaus.org', 'access.redhawk.org', 'bl.tiopan.com', 'blacklist.sci.kun.nl', 'blocked.hilli.dk', 'dnsbl.spfbl.net', 'dev.null.dk', 'dialups.mail-abuse.org', 'dnsbl.abuse.ch', 'dnsbl.antispam.or.id', 'dnsbl.justspam.org', 
# 'hil.habeas.com', 'mail-abuse.blacklist.jippg.org', 'msgid.bl.gweep.ca', 'no-more-funn.moensted.dk', 'opm.tornevall.org', 'pss.spambusters.org.ar', 'rbl.snark.net', 'spam.olsentech.net', 'bl.mailspike.net', 'blackholes.wirehub.net', 'block.dnsbl.sorbs.net', 'dialup.blacklist.jippg.org', 'dialups.visi.com', 'dnsbl.anticaptcha.net', 'dnsbl.kempt.net', 'dnsbl.tornevall.org', 'escalations.dnsbl.sorbs.net', 'black.junkemailfilter.com', 'intruders.docs.uu.se', 'new.dnsbl.sorbs.net', 'old.dnsbl.sorbs.net', 'rbl.schulte.org', 'recent.dnsbl.sorbs.net', 'relays.mail-abuse.org', 'rsbl.aupads.org', 'spamguard.leadmon.net']  
# )