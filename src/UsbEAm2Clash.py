#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser
import yaml
from pathlib import Path

def saveRules(name: str, domains: dict):
    f = Path('Clash/'+name.replace(' ', '_')+'.yaml')
    f.parent.mkdir(exist_ok=True, parents=True)
    f.write_text(yaml.dump({'payload': domains}, allow_unicode=True, indent=2), encoding='utf-8')

config = configparser.RawConfigParser()

# ref: https://github.com/dogfight360/UsbEAm/blob/master/Usbeam/usbeam_new_20.xml
config.read('UsbEAm.ini', encoding='utf-8')

groups = []
for name in config.sections():
    section = config[name]
    if 'ZH' in section:
        group = {}
        group['name'] = name
        group['nameZH'] = section['ZH']
        # group['group_id'] = section['Group_ID']
        ids = section['ID'].split(',')
        group['rules'] = []
        for id in ids:
            rulestring = section[id].split('|')
            rule = {}
            rule['name'] = rulestring[0]
            rule['nameZH'] = rulestring[1]
            rule['domains'] = rulestring[3].split(',')
            rule['tips'] = rulestring[4]
            rule['tipsZH'] = rulestring[5]
            rule['port'] = rulestring[6]
            group['rules'].append(rule)
        groups.append(group)

gamesDomains = []
gamesDownloadDOmains = []
for group in groups:
    gamingPlatform = ["Steam", "Epic", "EA", "Oragin", "Battle.net", "Uplay", "GOG", "Microsoft", "Riot", "Rockstar", "Other Platforms"]
    if any(platform in group['name'] for platform in gamingPlatform):
        domains = []
        downloadDomains = []
        onedriveDomains = []
        for rule in group['rules']:
            l = ['download', 'china', 'client', 'connection manager']
            if 'OneDrive' in rule['name']:
                onedriveDomains.extend(rule['domains'])
            elif any(x in rule['name'].lower() for x in l):
                downloadDomains.extend(rule['domains'])
            else:
                domains.extend(rule['domains'])
        saveRules(group['name'], domains)
        saveRules(group['name']+' Download', downloadDomains)
        saveRules('OneDrive', onedriveDomains)
        gamesDomains.extend(domains)
        gamesDownloadDOmains.extend(downloadDomains)
saveRules('Games', gamesDomains)
saveRules('Games Download', gamesDownloadDOmains)
