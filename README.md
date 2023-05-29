This is a fork of the [Hurricane Labs Machinae tool](https://github.com/HurricaneLabs/machinae) with some modifications to clean up output for use in personal projects.
If you're looking to use this library in a project, I recommend checking out the original Machinae repoistory.


Machinae Security Intelligence Collector
========================================

Machinae is a tool for collecting intelligence from public sites/feeds about
various security-related pieces of data: IP addresses, domain names, URLs,
email addresses, file hashes and SSL fingerprints. It was inspired by
[Automater](https://github.com/1aN0rmus/TekDefense-Automater), another excellent tool for collecting information. The Machinae
project was born from wishing to improve Automater in 4 areas:

1. Codebase - Bring Automater to python3 compatibility while making the code
more pythonic
1. Configuration - Use a more human readable configuration format (YAML)
2. Inputs - Support JSON parsing out-of-the-box without the need to write
regular expressions, but still support regex scraping when needed
1. Outputs - Support additional output types, including JSON, while making
extraneous output optional


Installation
------------

Machinae can be installed using pip3:

    pip3 install machinae

Or, if you're feeling adventurous, can be installed directly from github:

    pip3 install git+https://austinoneil.com/aoneil/machinae.git

You will need to have whatever dependencies are required on your system for
compiling Python modules (on Debian based systems, `python3-dev`), as well as
the libyaml development package (on Debian based systems, `libyaml-dev`).

You'll also want to grab the [latest configuration file](https://github.com/HurricaneLabs/machinae/raw/master/machinae.yml) and place it in
`/etc/machinae.yml`.


Configuration File
------------------

Machinae supports a simple configuration merging system to allow you to make
adjustments to the configuration without modifying the machinae.yml we provide
you, making configuration updates a snap. This is done by finding a system-wide
default configuration (default `/etc/machinae.yml`), merging into that a
system-wide local configuration (`/etc/machinae.local.yml`) and finally a
per-user local configuration (`~/.machinae.yml`). The system-wide configuration
can also be located in the current working directory, can be set using the
`MACHINAE_CONFIG` environment variable, or of course by using the `-c` or
`--config` command line options. Configuration merging can be disabled by
passing the `--nomerge` option, which will cause Machinae to only load the
default system-wide configuration (or the one passed on the command line).

As an example of this, say you'd like to enable the Fortinet Category site,
which is disabled by default. You could modify `/etc/machinae.yml`, but these
changes would be overwritten by an update. Instead, you can put the following
in either `/etc/machinae.local.yml` or `~/.machinae.yml`:

    fortinet_classify:
      default: true

Or, conversely, to disable a site, such as Virus Total pDNS:

    vt_ip:
      default: false
    vt_domain:
      default: false


Usage
-----

Machinae usage is very similar to Automater:

    usage: machinae [-h] [-c CONFIG] [--nomerge] [-d DELAY] [-f FILE] [-i INFILE] [-v]
                [-o {D,J,N,S}] [-O {ipv4,ipv6,fqdn,email,sslfp,hash,url}] [-q]
                [-s SITES] [-a AUTH] [-H HTTP_PROXY]
                [--dump-config | --detect-otype]
                ...

- See above for details on the `-c`/`--config` and `--nomerge` options.

- Machinae supports a `-d`/`--delay` option, like Automater. However, Machinae
uses 0 by default.

- Machinae output is controlled by two arguments:
    - `-o` controls the output format, and can be followed by a single character
	to indicated the desired type of output:
		- *N* is the default output ("Normal")
		- *D* is the default output, but dot characters are replaced
		- *J* is JSON output
	- `-f`/`--file` specifies the file where output should be written. The default
	is "-" for stdout.

- Machinae will attempt to auto-detect the type of target passed in (Machinae
refers to targets as "observables" and the type as "otype"). This detection can
be overridden with the `-O`/`--otype` option. The choices are listed in the
usage

- By default, Machinae operates in verbose mode. In this mode, it will output
status information about the services it is querying on the console as they are
queried. This output will always be written to stdout, regardless of the output
setting. To disable verbose mode, use `-q`

- By default, Machinae will run through all services in the configuration that
apply to each target's otype *and* are not marked as "default: false". To modify
this behavior, you can:
    - Pass a comma separated list of sites to run (use the top level key from the
	configuration).
	- Pass the special keyword `all` to run through all services *including* those
	marked as "default: false"

	Note that in both cases, `otype` validation is still applied.

- Machinae supports passing an HTTP proxy on the command line using the
`-H`/`--http-proxy` argument. If no proxy is specified, machinae will search the
standard `HTTP_PROXY` and `HTTPS_PROXY` environment variables, as well as the
less standard `http_proxy` and `https_proxy` environment variables.

- Lastly, a list of targets should be passed. All arguments other than the
options listed above will be interpreted as targets.


Out-of-the-Box Data Sources
---------------------------

Machinae comes with out-of-the-box support for the following data sources:

- IPVoid
- URLVoid
- URL Unshortener (http://www.toolsvoid.com/unshorten-url)
- Malc0de
- SANS
- FreeGeoIP (freegeoip.io)
- Fortinet Category
- VirusTotal pDNS (via web scrape - commented out)
- VirusTotal pDNS (via JSON API)
- VirusTotal URL Report (via JSON API)
- VirusTotal File Report (via JSON API)
- Reputation Authority
- ThreatExpert
- VxVault
- ProjectHoneypot
- McAfee Threat Intelligence
- StopForumSpam
- Cymru MHR
- ICSI Certificate Notary
- TotalHash (disabled by default)
- DomainTools Parsed Whois (Requires API key)
- DomainTools Reverse Whois (Requires API key)
- DomainTools Reputation
- IP WHOIS (Using RIR REST interfaces)
- Hacked IP
- Metadefender Cloud (Requires API key)
- GreyNoise (Requires API key)
- IBM XForce (Required API key)

Disabled by default
---------------------------

The following sites are disabled by default

- Fortinet Category (`fortinet_classify`)
- Telize Geo IP (`telize`)
- TotalHash (`totalhash_ip`)
- DomainTools Parsed Whois (`domaintools_parsed_whois`)
- DomainTools Reverse Whois (`domaintools_reverse_whois`)
- DomainTools Reputation (`domaintools_reputation`)
- PassiveTotal Passive DNS (`passivetotal_pdns`)
- PassiveTotal Whois (`passivetotal_whois`)
- PassiveTotal SSL Certificate History (`passivetotal_sslcert`)
- PassiveTotal Host Attribute Components (`passivetotal_components`)
- PassiveTotal Host Attribute Trackers (`passivetotal_trackers`)
- MaxMind GeoIP2 Passive Insight (`maxmind`)
- FraudGuard (`fraudguard`)
- Shodan (`shodan`)
- Hacked IP
- Metadefender Cloud (Requires API key)
- GreyNoise (Requires API key)
- IBM XForce (Requires API key)

HTTP Basic Authentication and Configuration
-------------------------------------------

Machinae supports HTTP Basic Auth for sites that require it through the `--auth/-a`
flag. You will need to create a YAML file with your credentials, which will include
a key to the site that requires the credentials and a list of two items, username
and password or API key. For example, for the included PassiveTotal site this might
look like:

    passivetotal: ['myemail@example.com', 'my_api_key']

Inside the site configuration under `request` you will see a key such as:

    json:
      request:
        url: '...'
        auth: passivetotal

The `auth: passivetotal` points to the key inside the authentication config passed
via the command line.

Output Formats
--------------

Machinae comes with a limited set of output formats: normal, normal with dot
escaping, and JSON. We plan to add additional output formats in the future.

License Info
------------

The MIT License (MIT)

Copyright (c) 2015 Hurricane Labs LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
