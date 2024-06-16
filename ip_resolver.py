import socket
import re

domain_list = ['blogger.googleapis.com', 'migrationcenter.googleapis.com', 'abusiveexperiencereport.googleapis.com',
               'baremetalsolution.googleapis.com', 'chromepolicy.googleapis.com', 'keep.googleapis.com',
               'analyticsadmin.googleapis.com', 'speech.googleapis.com', 'addressvalidation.googleapis.com',
               'compute.googleapis.com', 'dataflow.googleapis.com', 'adsense.googleapis.com',
               'firebaserules.googleapis.com', 'notebooks.googleapis.com', 'sts.googleapis.com',
               'recommendationengine.googleapis.com', 'datastream.googleapis.com', 'digitalassetlinks.googleapis.com',
               'alertcenter.googleapis.com', 'integrations.googleapis.com', 'classroom.googleapis.com',
               'cloudsupport.googleapis.com', 'mybusinessverifications.googleapis.com', 'playgrouping.googleapis.com',
               'smartdevicemanagement.googleapis.com', 'vpcaccess.googleapis.com', 'androidmanagement.googleapis.com',
               'gkeonprem.googleapis.com', 'licensing.googleapis.com', 'trafficdirector.googleapis.com',
               'publicca.googleapis.com', 'driveactivity.googleapis.com', 'dataplex.googleapis.com',
               'forms.googleapis.com', 'dns.googleapis.com', 'adexperiencereport.googleapis.com',
               'recaptchaenterprise.googleapis.com', 'vision.googleapis.com', 'cloudtasks.googleapis.com',
               'osconfig.googleapis.com', 'drivelabels.googleapis.com', 'apikeys.googleapis.com', 'ids.googleapis.com',
               'mybusinesslodging.googleapis.com', 'pubsublite.googleapis.com',
               'readerrevenuesubscriptionlinking.googleapis.com', 'servicemanagement.googleapis.com',
               'airquality.googleapis.com', 'chat.googleapis.com', 'datastore.googleapis.com',
               'documentai.googleapis.com', 'dataportability.googleapis.com', 'videointelligence.googleapis.com',
               'contactcenterinsights.googleapis.com', 'gkehub.googleapis.com', 'composer.googleapis.com',
               'appengine.googleapis.com', 'analytics.googleapis.com', 'mybusinessnotifications.googleapis.com',
               'batch.googleapis.com', 'policyanalyzer.googleapis.com', 'androiddeviceprovisioning.googleapis.com',
               'apigeeregistry.googleapis.com', 'gamesconfiguration.googleapis.com', 'ondemandscanning.googleapis.com',
               'iamcredentials.googleapis.com', 'orgpolicy.googleapis.com', 'vmwareengine.googleapis.com',
               'admob.googleapis.com', 'dialogflow.googleapis.com', 'datafusion.googleapis.com',
               'doubleclicksearch.googleapis.com', 'eventarc.googleapis.com', 'accessapproval.googleapis.com',
               'apphub.googleapis.com', 'libraryagent.googleapis.com', 'analyticsdata.googleapis.com',
               'privateca.googleapis.com', 'checks.googleapis.com', 'mybusinessbusinessinformation.googleapis.com',
               'run.googleapis.com', 'sqladmin.googleapis.com', 'texttospeech.googleapis.com',
               'pagespeedonline.googleapis.com', 'bigquerydatatransfer.googleapis.com', 'pubsub.googleapis.com',
               'sasportal.googleapis.com', 'contentwarehouse.googleapis.com', 'toolresults.googleapis.com',
               'youtubeanalytics.googleapis.com', 'places.googleapis.com',
               'paymentsresellersubscription.googleapis.com', 'jobs.googleapis.com',
               'certificatemanager.googleapis.com', 'apigee.googleapis.com', 'cloudfunctions.googleapis.com',
               'shoppingcontent.googleapis.com', 'localservices.googleapis.com', 'blockchainnodeengine.googleapis.com',
               'identitytoolkit.googleapis.com', 'tasks.googleapis.com', 'secretmanager.googleapis.com',
               'bigtableadmin.googleapis.com', 'firebaseappdistribution.googleapis.com',
               'chromemanagement.googleapis.com', 'biglake.googleapis.com', 'domainsrdap.googleapis.com',
               'analyticsreporting.googleapis.com', 'firebasestorage.googleapis.com', 'gkebackup.googleapis.com',
               'kgsearch.googleapis.com', 'people.googleapis.com', 'sheets.googleapis.com', 'transcoder.googleapis.com',
               'cloudprofiler.googleapis.com', 'adexchangebuyer.googleapis.com',
               'mybusinessaccountmanagement.googleapis.com', 'spanner.googleapis.com',
               'developerconnect.googleapis.com', 'gamesmanagement.googleapis.com',
               'advisorynotifications.googleapis.com', 'workflows.googleapis.com', 'androidenterprise.googleapis.com',
               'fcm.googleapis.com', 'beyondcorp.googleapis.com', 'policytroubleshooter.googleapis.com',
               'servicedirectory.googleapis.com', 'acceleratedmobilepageurl.googleapis.com',
               'mybusinessqanda.googleapis.com', 'reseller.googleapis.com', 'youtube.googleapis.com',
               'cloudbilling.googleapis.com', 'gmailpostmastertools.googleapis.com', 'retail.googleapis.com',
               'streetviewpublish.googleapis.com', 'www.googleapis.com', 'iam.googleapis.com',
               'clouderrorreporting.googleapis.com', 'firebase.googleapis.com', 'mybusinessplaceactions.googleapis.com',
               'iap.googleapis.com', 'walletobjects.googleapis.com', 'deploymentmanager.googleapis.com',
               'safebrowsing.googleapis.com', 'cloudkms.googleapis.com', 'billingbudgets.googleapis.com',
               'cloudchannel.googleapis.com', 'sourcerepo.googleapis.com', 'cloudtrace.googleapis.com',
               'manufacturers.googleapis.com', 'playcustomapp.googleapis.com', 'displayvideo.googleapis.com',
               'healthcare.googleapis.com', 'datamigration.googleapis.com', 'dataproc.googleapis.com',
               'groupsmigration.googleapis.com', 'servicecontrol.googleapis.com', 'slides.googleapis.com',
               'tpu.googleapis.com', 'firebasedynamiclinks.googleapis.com', 'cloudsearch.googleapis.com',
               'analyticshub.googleapis.com', 'aiplatform.googleapis.com', 'lifesciences.googleapis.com',
               'civicinfo.googleapis.com', 'networkservices.googleapis.com', 'resourcesettings.googleapis.com',
               'playdeveloperreporting.googleapis.com', 'storage.googleapis.com', 'androidpublisher.googleapis.com',
               'searchads360.googleapis.com', 'containeranalysis.googleapis.com', 'translation.googleapis.com',
               'metastore.googleapis.com', 'travelimpactmodel.googleapis.com', 'workloadmanager.googleapis.com',
               'bigquery.googleapis.com', 'binaryauthorization.googleapis.com', 'servicenetworking.googleapis.com',
               'assuredworkloads.googleapis.com', 'webrisk.googleapis.com', 'script.googleapis.com',
               'webfonts.googleapis.com', 'storagetransfer.googleapis.com', 'workspaceevents.googleapis.com',
               'factchecktools.googleapis.com', 'bigquerydatapolicy.googleapis.com', 'cloudbuild.googleapis.com',
               'cloudresourcemanager.googleapis.com', 'backupdr.googleapis.com', 'datalabeling.googleapis.com',
               'firebasehosting.googleapis.com', 'networkmanagement.googleapis.com', 'discoveryengine.googleapis.com',
               'tagmanager.googleapis.com', 'looker.googleapis.com', 'datapipelines.googleapis.com',
               'homegraph.googleapis.com', 'indexing.googleapis.com', 'doubleclickbidmanager.googleapis.com',
               'customsearch.googleapis.com', 'ml.googleapis.com', 'logging.googleapis.com', 'firestore.googleapis.com',
               'cloudscheduler.googleapis.com', 'file.googleapis.com', 'vmmigration.googleapis.com',
               'securitycenter.googleapis.com', 'verifiedaccess.googleapis.com', 'serviceusage.googleapis.com',
               'firebaseappcheck.googleapis.com', 'chromeuxreport.googleapis.com', 'fitness.googleapis.com',
               'kmsinventory.googleapis.com', 'dataform.googleapis.com', 'fcmdata.googleapis.com',
               'prod-tt-sasportal.googleapis.com', 'realtimebidding.googleapis.com', 'runtimeconfig.googleapis.com',
               'youtubereporting.googleapis.com', 'games.googleapis.com', 'websecurityscanner.googleapis.com',
               'marketingplatformadmin.googleapis.com', 'dlp.googleapis.com', 'alloydb.googleapis.com',
               'businessprofileperformance.googleapis.com', 'cloudidentity.googleapis.com',
               'cloudcontrolspartner.googleapis.com', 'docs.googleapis.com', 'playintegrity.googleapis.com',
               'language.googleapis.com', 'oslogin.googleapis.com', 'bigqueryreservation.googleapis.com',
               'bigqueryconnection.googleapis.com', 'networkconnectivity.googleapis.com',
               'contactcenteraiplatform.googleapis.com', 'solar.googleapis.com', 'accesscontextmanager.googleapis.com',
               'acmedns.googleapis.com', 'essentialcontacts.googleapis.com', 'books.googleapis.com',
               'networksecurity.googleapis.com', 'connectors.googleapis.com', 'gmail.googleapis.com',
               'recommender.googleapis.com', 'policysimulator.googleapis.com', 'versionhistory.googleapis.com',
               'workstations.googleapis.com', 'area120tables.googleapis.com', 'config.googleapis.com',
               'datalineage.googleapis.com', 'memcache.googleapis.com', 'admin.googleapis.com',
               'container.googleapis.com', 'searchconsole.googleapis.com', 'vault.googleapis.com',
               'workflowexecutions.googleapis.com', 'rapidmigrationassessment.googleapis.com',
               'clouddeploy.googleapis.com', 'redis.googleapis.com', 'artifactregistry.googleapis.com',
               'apigateway.googleapis.com', 'firebasedatabase.googleapis.com', 'managedidentities.googleapis.com',
               'serviceconsumermanagement.googleapis.com', 'testing.googleapis.com', 'cloudasset.googleapis.com',
               'firebaseml.googleapis.com', 'domains.googleapis.com', 'dfareporting.googleapis.com',
               'datacatalog.googleapis.com', 'authorizedbuyersmarketplace.googleapis.com', 'monitoring.googleapis.com',
               'cloudshell.googleapis.com', 'accounts.google.com', 'tunnel.cloudproxy.app']


def is_ipv4(ip):
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return pattern.match(ip) is not None


def resolve_domain_all_ips(domain_name):
    try:
        result = socket.gethostbyname_ex(domain_name)
        ip_addresses = result[2]
        return [ip for ip in ip_addresses if is_ipv4(ip)]
    except socket.gaierror as e:
        print(f"Error resolving domain {domain_name}: {e}")
        return []


def get_domain_list():
    return domain_list


def write_ips_to_file(file_path, ip_addresses):
    try:
        with open(file_path, 'r') as file:
            existing_ips = file.read().splitlines()
    except FileNotFoundError:
        existing_ips = []

    existing_ipv4_ips = [ip for ip in existing_ips if is_ipv4(ip)]
    all_ips = set(existing_ipv4_ips) | set(ip_addresses)
    sorted_ips = sorted(all_ips)

    try:
        with open(file_path, 'w') as file:
            file.write('\n'.join(sorted_ips))
    except IOError as e:
        print(f"Error writing file {file_path}: {e}")

    return sorted_ips
