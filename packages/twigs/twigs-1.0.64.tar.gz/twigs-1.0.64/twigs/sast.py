import sys
import re
import os
import shutil
import stat
import subprocess
import logging
import json
import tempfile
import traceback

sast_plugin = "/usr/local/bin/semgrep"

def on_rm_error( func, path, exc_info):
    os.chmod( path, stat.S_IWRITE )
    os.unlink( path )

def get_rating(severity):
    if severity == 'ERROR':
        return '4'
    if severity == 'WARNING':
        return '3'
    return '1'

def get_description(result):
    desc = result['extra']['message']
    if 'fix' in result['extra']:
        desc = desc + '\n' + 'Suggested fix: '+result['extra']['fix']
    if 'metadata' in result['extra']:
        if 'cwe' in result['extra']['metadata']:
            desc = desc + '\n' + 'CWE: '+result['extra']['metadata']['cwe']
        if 'owasp' in result['extra']['metadata']:
            desc = desc + '\n' + 'OWASP: '+result['extra']['metadata']['owasp']
        if 'references' in result['extra']['metadata']:
            for ref in result['extra']['metadata']['references']:
                desc = desc + '\n' + ref
    return desc

def run_sast(args, path, base_path):
    findings = []
    if not os.path.isfile(sast_plugin) or not os.access(sast_plugin, os.X_OK):
        logging.error('SAST plugin CLI - semgrep not found')
        sys.exit(1) 

    params = ' -q --json --config=p/r2c-security-audit ' + path
    
    cmdarr = [sast_plugin+ " " + params]
    sast_issues = None
    try:
        out = subprocess.check_output(cmdarr, shell=True)
        sast_issues = json.loads(out)
    except subprocess.CalledProcessError:
        logging.error("Error running SAST CLI semgrep")
        shutil.rmtree(path, onerror = on_rm_error)
        return None 
    logging.info("SAST checks completed")

    results = sast_issues['results']
    for r in results:
        finding = {}
        finding['issue_id'] = r['check_id']
        finding['rating'] = get_rating(r['extra']['severity'])
        finding['filename'] = r['path'].replace(base_path,'')
        if args.no_code:
            finding['code_snippet'] = ''
        else:
            finding['code_snippet'] = r['extra']['lines']
        finding['lineno_start'] = r['start']['line']
        finding['lineno_end'] = r['end']['line']
        finding['description'] = get_description(r)
        finding['cwe'] = ''
        finding['owasp'] = ''
        if 'metadata' in r['extra']:
            if 'cwe' in r['extra']['metadata']:
                finding['cwe'] = r['extra']['metadata']['cwe']
            if 'owasp' in r['extra']['metadata']:
                finding['owasp'] = r['extra']['metadata']['owasp']
        findings.append(finding)

    #print json.dumps(findings, indent=4)
    return findings
