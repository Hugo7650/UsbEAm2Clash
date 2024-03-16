#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser
import yaml
from pathlib import Path

gamingPlatform = ["Steam", "Epic", "EA", "Oragin", "Battle.net", "Uplay", "GOG", "Microsoft", "Riot", "Rockstar", "Other Platforms", "Nintendo", "Xbox", "Playstation"]

def saveRules(name: str, domains: list):
    f = Path('Clash/'+name.replace(' ', '_')+'.yaml')
    f.parent.mkdir(exist_ok=True, parents=True)
    f.write_text(yaml.dump({'payload': domains}, allow_unicode=True, indent=2), encoding='utf-8')

def getGroup(config):
    groups = []
    for name in config.sections():
        section = config[name]
        if 'ZH' in section:
            group = {}
            group['name'] = name
            group['nameZH'] = section['ZH']
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
    return groups

def parseGroup(group):
    gamesDomains = []
    gamesDownloadDOmains = []
    for group in groups:
        if any(platform in group['name'] for platform in gamingPlatform):
            domains = []
            downloadDomains = []
            onedriveDomains = []
            keywords = ['download', 'china', 'client', 'connection manager']
            for rule in group['rules']:
                if 'Microsoft' in group['name'] and 'OneDrive' in rule['name']:
                    onedriveDomains.extend(rule['domains'])
                elif any(keyword in rule['name'].lower() for keyword in keywords) and "discord" not in rule['name'].lower():
                    downloadDomains.extend(rule['domains'])
                else:
                    domains.extend(rule['domains'])
            saveRules(group['name'], domains)
            saveRules(group['name']+' Download', downloadDomains)
            if 'Microsoft' in group['name']:
                saveRules('OneDrive', onedriveDomains)
            gamesDomains.extend(domains)
            gamesDownloadDOmains.extend(downloadDomains)
    saveRules('Games', gamesDomains)
    saveRules('Games Download', gamesDownloadDOmains)

config = configparser.RawConfigParser()
config_console = configparser.ConfigParser()

# ref: https://github.com/dogfight360/UsbEAm/blob/master/Usbeam/usbeam_new_20.xml
config.read('UsbEAm.ini', encoding='utf-8')
config_console.read('UsbEAm_console.ini', encoding='utf-8')

groups = getGroup(config) + getGroup(config_console)

parseGroup(groups)
