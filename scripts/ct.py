import os
import concurrent.futures

def run_theharvester(email):
    domain = email.split("@")[-1]
    command = f"python3 ~/Desktop/cleartrace/tools/theHarvester/theHarvester.py -d {domain} -b all"
    try:
        result = os.popen(command).read()
        return {"tool": "theHarvester", "data": result}
    except Exception as e:
        return {"tool": "theHarvester", "data": f"Error: {str(e)}"}

def run_spiderfoot(email):
    command = f"python3 ~/Desktop/cleartrace/tools/spiderfoot/sf.py -s {email} -m sfp_email,sfp_breach -o tab"
    try:
        result = os.popen(command).read()
        return {"tool": "SpiderFoot", "data": result}
    except Exception as e:
        return {"tool": "SpiderFoot", "data": f"Error: {str(e)}"}

def run_holehe(email):
    command = f"holehe {email}"
    try:
        result = os.popen(command).read()
        return {"tool": "Holehe", "data": result}
    except Exception as e:
        return {"tool": "Holehe", "data": f"Error: {str(e)}"}

def run_sherlock(email):
    username = email.split("@")[0]
    command = f"sherlock {username} --timeout 10"
    try:
        result = os.popen(command).read()
        return {"tool": "Sherlock", "data": result}
    except Exception as e:
        return {"tool": "Sherlock", "data": f"Error: {str(e)}"}

def run_osint_tools(email):
    """Run all OSINT tools and return their results."""
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(run_theharvester, email),
            executor.submit(run_spiderfoot, email),
            executor.submit(run_holehe, email),
            executor.submit(run_sherlock, email)
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results