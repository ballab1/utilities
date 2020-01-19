TODO
```

get working
 - docker-search.py
 
improve
  deploy : 
    - recognize 'secrets'
    - recognize 'container_os' as none, or missing
    - split app.setup: 
    	move init function into deploy and call app.init
    	move common functions into deploy and call app.common


implement ability to create/update github webhook
 - also add graphql

implement Docker.findImage  (should check local and remote. Need flag to indicate to pull remote)
move to python:3.7


security
    remove CBF bashlib exports:  implement registry (using grep) of functions, and export when needed


docker-utilities
    retagimages should be specific to build_PDR directory, deploy directory or a docker-compose.yml
    getimage should update 'versions' folder
    pushImage needs to be able to rename to latest if needed
    registry report
      - include packed sizes
    implement wildcards on pushimage
    docker-registry
        - change to https
        - configure to use redis
             https://github.com/docker-library/redis/blob/e95c0cf4ffd9a52aa48d05b93fe3b42069c05032/5.0-rc/32bit/Dockerfile


deploy
    allow version overrides for any service
        should be able to specify (and replace in docker-compose.yml) a 'named' container_tag
    when CONTAINER_TAG coresponds to git tag (may need to use --promote), put tag into docker-compose rather than fingerprint
        set default CONTAINER_TAG to tag
        push images with tag=CONTAINER_TAG
        set tag on current repo (if not exists)
    capture container image ID's before down, and check for orphaned ID's after up
    git login required even on 'down'
    retag existing images if (needed and ! inuse)
    recognize ">>>>> issue while executing 06.nagios <<<<<" 
    add docker-compose checking to deploy



builds
    optionally push 'latest'
    quality ladder:  dev -> staging -> master
        - deploy should set 'latest' (not build). (use registry API to get and work with available images)
        - dev:  where we make changes
        - staging: PRs from dev + CI builds
        - master: production
    fix promotions: quality ladder:  dev -> staging -> master
            - keep dev at 1 build
            - deploy should update 'latest' tag
    Separate build, package and deploy/run actions
        Fix up docker dependency script

Errors

	docker-search.py
	==================================================================================
	docker-search.py eebd9804d7717a5c46a30006430b9394001bba5ec882a5df390a112355a84bea
	    DockerVolume instance has no attribute 'id'
	    Traceback (most recent call last):
	      File "/home/bobb/.bin/docker-search.py", line 836, in main
		volumes.find(str_ref)
	      File "/home/bobb/.bin/docker-search.py", line 610, in find
		self.matches[volume.id] = volume
	    AttributeError: DockerVolume instance has no attribute 'id'



	docker-utilities
	==================================================================================

	deleting devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f  202
	restoring tags:
	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:latest

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:e299bfda7f249ccf3aa50b8fbd96c6bd448102659e97522fb81b6bbe876d9912
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:e299bfda7f249ccf3aa50b8fbd96c6bd448102659e97522fb81b6bbe876d9912
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:e299bfda7f249ccf3aa50b8fbd96c6bd448102659e97522fb81b6bbe876d9912

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:a79a8d8484c7591094705f30e2c9c22d3730e9db755c44100d5bc9108a3aecaf
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:a79a8d8484c7591094705f30e2c9c22d3730e9db755c44100d5bc9108a3aecaf
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:a79a8d8484c7591094705f30e2c9c22d3730e9db755c44100d5bc9108a3aecaf

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:88f8ce68cab5af39225903a0e2dba7190e9b9c03c4c31194c53a59046e6d48e3
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:88f8ce68cab5af39225903a0e2dba7190e9b9c03c4c31194c53a59046e6d48e3
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:88f8ce68cab5af39225903a0e2dba7190e9b9c03c4c31194c53a59046e6d48e3

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:838e7102a7176cfdc2cc07fd6003c8b8dc867d40e3a682a3adc518509871341f
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:838e7102a7176cfdc2cc07fd6003c8b8dc867d40e3a682a3adc518509871341f
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:838e7102a7176cfdc2cc07fd6003c8b8dc867d40e3a682a3adc518509871341f

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:81fad85738b2a8677ec6b56cc8b468bad0df4448f16155c748af125749239260
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:81fad85738b2a8677ec6b56cc8b468bad0df4448f16155c748af125749239260
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:81fad85738b2a8677ec6b56cc8b468bad0df4448f16155c748af125749239260

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:3159f68306a550f87694136f3ea967bca2161a5292c762a78ff6e5d402d0574d
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:3159f68306a550f87694136f3ea967bca2161a5292c762a78ff6e5d402d0574d
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:3159f68306a550f87694136f3ea967bca2161a5292c762a78ff6e5d402d0574d

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:28deda57ff286ca7eb26b819036e627bda63853566ffd21753866fb1617e42de
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:28deda57ff286ca7eb26b819036e627bda63853566ffd21753866fb1617e42de
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:28deda57ff286ca7eb26b819036e627bda63853566ffd21753866fb1617e42de

	pushing ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:v4.2
	Error response from daemon: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4@sha256:329c659449b142a2149adbaa63e4fb08c18405e3f5630fc90bc1e0ad08f7e62f
	tag does not exist: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:v4.2
	Error: No such image: ubuntu-s2:5000/devops/alpine/phpmyadmin/4.8.4:v4.2

	Elapsed time: 01:23:16
	==================================================================================


Done
=============================================================
```
01/18/2020
  deploy : 
    - recognize 'thirdparty_versions'
    - reduce 'skip_wait' - auto include any which are not CBF (chack using docker labels)


12/15/2019
docker-utilities
    Unable to load libraries
         docker-utilities report --format json --output /opt/registryContents.json
    error running
        ..executing /usr/local/crf/startup/99.logs.sh
            sourcing (CRF):  CRF 01.dockr
            adding dir: /var/log, uid: 1000 to cache_file: /tmp/fixUpCache
            Fixing up directory: /var/log  for user: builder(1000)
             - changing ownership for directory: /var/log  to 1000:builder
        chmod: cannot operate on dangling symlink '/usr/local/bin/appenv.bashlib'
        ***ERROR at /usr/local/crf/bashlib/crf.bashlib:257. 'chmod a+rx "/usr/local/bin/"*' exited with status 1
        ***ERROR at /usr/local/bin/docker-entrypoint.sh:88. 'tee -a "$logFile" 1>&2' exited with status 1
        ***ERROR at /usr/local/bin/docker-entrypoint.sh:21. 'sudo -E "$0" "$config_entry"' exited with status 1
        ***ERROR at /usr/local/bin/docker-entrypoint.sh:74. 'tee -a "$logFile" 1>&2' exited with status 1

	build.sh
	==================================================================================
	building ubuntu-s2:5000/devops/ubuntu/confluent/5.3.1:dev
	    refs:           (HEAD -> dev/ballab1/f4072, origin/dev/ballab1/f4072)
	    commitId:       3b1d9e48fa64d7873036991c07d16201721e0732
	    repo:           https://eos2git.cec.lab.emc.com/Devops/confluent_container
	    fingerprint:    42cc0320bcd221d7f1acf16018fd9f46b457455e751f99733b7d1baf0c3385bb
	    revision:       v0.0-1-g3b1d9e4
	    parent:         ubuntu-s2:5000/devops/ubuntu/openjdk/1.8.0_181:f0d337f73be4f37fe432bc254167a66a96c30220fe0b7a6a0ef2dbd276a0f643
	    BASE_TAG:       dev
	    checking for local ubuntu-s2:5000/devops/ubuntu/confluent/5.3.1:dev with the correct fingerprint
	    ubuntu-s2:5000/devops/ubuntu/confluent/5.3.1:dev has not changed.
	    duration:       00:00:06
	KAFKA_BOOTSTRAP_SERVERS not defined. No metrics gathered




11/29/2019
deploy
    change to deploy.yml

11/9/2019
builds
    recognize parent on different branch
	    prompt to pull dependant images and retag
    add user/settings credential support

11/2/2019
deploy
    add user/settings credential support
    regression: CONTAINER_TAG always honored, may have other side effects
    bugtrace:
	    cyc@hopcyc-ballab1-1-00 ~/GIT/devops_container_environment (dev/ballab1/mres3291)
	    $ ./deploy --clean
	    ***ERROR at /home/cyc/GIT/devops_container_environment/libs/deploy.bashlib:95. 'grep -cs "$network"' exited with status 1
	    >>>    Current directory /home/cyc/GIT/devops_container_environment
	    Stack trace:
	    >>>    01: /home/cyc/GIT/devops_container_environment/libs/deploy.bashlib:95 trap.catch_error  <<<
	    >>>    02: /home/cyc/GIT/devops_container_environment/libs/deploy.bashlib:331 deploy.clean  <<<
	    >>>    03: ./deploy:78 deploy.main  <<<
	    $rm -rf /home/cyc/GIT/devops_container_environment/workspace.devops_container_environment
	    $deploy.restart 2>&1 | tee restart.log
	    INFO: updating /home/cyc/GIT/devops_container_environment/workspace.devops_container_environment/docker-compose.yml
	    populating secrets

	    the following also reported because of interference with CFG_USER_SECRETS=~/.inf
	    ***ERROR: Password file: '.secrets/grafana_admin.pwd' not found. Used by startup of service: grafana
	    ***ERROR: Password file: '.secrets/mysql_root.pwd' not found. Used by startup of service: mysql
	    ***ERROR: Password file: '.secrets/mysql.pwd' not found. Used by startup of service: nagios
	    >> GENERATING SSL CERT
    update of ${CONFIG_DIR}/docker-compose.yml should only update 'image:'
docker-utilities
    registory curation
    add user/settings credential support
    need more help info in context help
    bugtrace:
	$ docker-utilities deleteTag 'devops/.*:dev' -u svc_cyclonebuild -c $__SETTINGS_FILE
	delete specific tag from ubuntu-s2:5000/ : devops/.*:dev
	retrieving digests for devops/.*
	***ERROR: failure to complete registry request
	    command:       curl --insecure --request GET --silent https://ubuntu-s2:5000/artifactory/api/docker/cyclone-dockerv2-local/v2/devops/.*/tags/list
	    error code:    "NAME_UNKNOWN"
	    error message: "Repository name not known to registry."
	    error details: {
	  "name": "devops/.*"
	}
	    http_code:     404 Not Found
	    Failed to get https://ubuntu-s2:5000/artifactory/api/docker/cyclone-dockerv2-local/v2/devops/.*/tags/list

	***ERROR: repository: devops/.* - does not exist


2019-10-04
docker-utilities
    deletetag --allrepos fails when a tag does not exist in a nrepo
    minor issue:
	$ docker-utilities report -o x.txt -f text
	docker-utilities: invalid option -- 'f'
	report remote images in ubuntu-s2:5000/  : text

	No content specified
	Caught: groovy.json.JsonException: Unable to determine the current character, it is not a string, number, array, or object

	The current character read is '}' with an int value of 125
	Unable to determine the current character, it is not a string, number, array, or object
	line number 1
	index number 8
	{"data":}
	........^
	groovy.json.JsonException: Unable to determine the current character, it is not a string, number, array, or object

	The current character read is '}' with an int value of 125
	Unable to determine the current character, it is not a string, number, array, or object
	line number 1
	index number 8
	{"data":}
	........^
		at org.apache.groovy.json.internal.JsonParserCharArray.decodeValueInternal(JsonParserCharArray.java:206)
		at org.apache.groovy.json.internal.JsonParserCharArray.decodeJsonObject(JsonParserCharArray.java:132)
		at org.apache.groovy.json.internal.JsonParserCharArray.decodeValueInternal(JsonParserCharArray.java:186)
		at org.apache.groovy.json.internal.JsonParserCharArray.decodeValue(JsonParserCharArray.java:157)


2019-09-07
docker-utilities 
    multiple updates
    recognize filer on tags for 'docker-utilities images '*:*'
deploy
    --container_tag needed. 


2019-07-07
    provide 'updateDownload'
            - download file
            - calc sha256
            - upload file to artifactory
            - update action_folders/04.downloads/
    docker-search
     - include sizes
     - layers: include count
     - dependants: include count
       docker-dependents: show labels for images
    docker-registry
    : registry
    : deleteImage: when deleting a repo, 202 is shown, but none of images or tags shown
        - handle more tags to fingerprint lookup (ex: latest, master, staging)
        - move old named content to new repos
        - permit deleteion of content based on
                tag  (as in all tags which match ... in a repo)
                do not use 'master' but instead 'yyyymmdd-$(git-describe)' and update docker-compose
        scan and reduce all entries to max
        scan and remove fingerprints 'from' n-x repos unless tags > 1
        remove specific tag (needs testing)
        add more docker registry management
            - delete tag from multiple repos
            - squash repo when new version created
            - other repo reports (what needs squashing, tags in use/where, image sizes and space reuse)
            - deploy for 'git describe' container; finish deploy workflow
            - handle more tags to fingerprint lookup (ex: latest, master, staging)
            - move old named content to new repos
            - permit deletion of content based on
                    tag  (as in all tags which match ... in a repo)
                    do not use 'master' but instead 'yyyymmdd-$(git-describe)' and update docker-compose


2019-06-15
registryReport (summary):
        add time
        add amount of space used

2019-05-26
docker-dependants: change to annon associative arrays
add registry analysis to report

docker-registry
- setup private docker registry
- improve error handling
- curate content on the fly
security
- mapping layer for ENV variables.  use docker-compose.yml
- base set going into docker-compose.yml : individual set for each container
- need layered containers
  permit removal of any environment variable prior to running service
  remove bashlib functions prior to running service

build
- consolidate setupProduction and restartProd

issues pushing/pulling to registry
     sometimes ':latest' not defined, sometimes 'fingerprint' not defined                
     projects should have definition of /version:tags
         so we can have
                jenkins/2.121.2:latest
                jenkins/2.121.3:latest
                jenkins:latest
     need a way to 'just push'

```
