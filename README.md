## INTERNSHIP - PROJECT

Automated malware collection and classification with signature based scan.

### Malware Sources

* [Malshare](https://malshare.com)
* [Malakel](http://malwaredb.malekal.com/index.php?page=1) => It is not being updated (Cumulative downloader will be written for contribution to database)
* [Malc0de](http://malc0de.com/database/)
* [Cybercrime-Tracker](https://cybercrime-tracker.net/)
* [VX-Vault](http://vxvault.net/ViriList.php)
* [Hybrid Analysis](https://hybrid-analysis.com)
* [Any.Run](https://app.any.run/submissions)
* [Tracker-h3x](http://tracker.h3x.eu/about/400)

### Yara rule sources

* [Yara-Rules](https://github.com/Yara-Rules/rules)
* [Neo23xO](https://github.com/Neo23x0/signature-base/tree/master/yara)
* [kevthehermit](https://github.com/kevthehermit/RATDecoders/tree/master/yaraRules)

### Workflow of YARA rule collection

* Yara rules will be collected from source or added manually based on personal analysis of samples.
* When a new rule is gathered, old **undetected** samples will be checked again with new rules.


### Workflow of Scanner

* New malwares will be checked and hashes will be written to database at certain frequency(probably daily)
* If sample doesn't exist in database it will be pulled.
* Pulled samples will be scanned with yara rules and detections will be saved database.


#### Possible additional features

* All samples' ssdeep values can be written into database and **undetected** samples' ssdeep values can be compared to detected ones.
* 