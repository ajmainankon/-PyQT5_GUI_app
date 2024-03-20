import json

# test data
cve1 = dict(CVE="CVE-2018-15664",
            Description="In Docker through 18.06.1-ce-rc2, the API endpoints behind the 'docker cp' command are "
                        "vulnerable to a symlink-exchange attack with Directory Traversal, giving attackers arbitrary "
                        "read-write access to the host filesystem with root privileges, because daemon/archive.go does "
                        "not do archive operations on a frozen filesystem (or from within a chroot).",
            CVSS=6.2,
            Link="https://www.cvedetails.com/cve/CVE-2018-15664/",
            Script='CVE-2018-15664.py')

cve2 = dict(CVE="CVE-2018-10892",
            Description="The default OCI linux spec in oci/defaults{_linux}.go in Docker/Moby from 1.11 to current "
                        "does not block /proc/acpi pathnames. The flaw allows an attacker to modify host's hardware "
                        "like enabling/disabling bluetooth or turning up/down keyboard brightness.",
            CVSS=5.0,
            Link="https://www.cvedetails.com/cve/CVE-2018-10892/",
            Script='CVE-2018-10892.py')
cve3 = dict(CVE="CVE-2019-5736",
            Description= "To-Do",
            CVSS=0.0,
            Link="To-Do",
            Script='CVE-2019-5736.py')

cve3 = dict(CVE="CVE-2019-5736",
            Description= "To-Do",
            CVSS=0.0,
            Link="To-Do",
            Script='CVE-2019-5736.py')
cve4 = dict(CVE="CVE-2019-13139",
            Description= "To-Do",
            CVSS=0.0,
            Link="To-Do",
            Script='CVE-2019-13139.py')
cve5 = dict(CVE="CVE-2019-14271 ",
            Description= "To-Do",
            CVSS=0.0,
            Link="To-Do",
            Script='CVE-2019-14271.py')


data = [cve1, cve2, cve3, cve4, cve5]
# json_str = json.dumps(data)

# write into json file
with open('test_data.json', 'w') as f:
        json.dump(data, f)