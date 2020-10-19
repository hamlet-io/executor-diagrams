from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.generic.storage import Storage
from diagrams.generic.blank import Blank
from diagrams.onprem.client import Client, User

# aws resources
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.general import TradicionalServer, GenericSamlToken
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SQS
from diagrams.aws.devtools import CommandLineInterface
from diagrams.aws.management import Cloudformation
from diagrams.aws.general import TradicionalServer
from diagrams.aws.security import IdentityAndAccessManagementIam, IdentityAndAccessManagementIamRole, IdentityAndAccessManagementIamAWSSts
from diagrams.aws.storage import ElasticFileSystemEFS
from diagrams.aws.network import CloudMap, CloudFront
from diagrams.aws.integration import ConsoleMobileApplication, SimpleNotificationServiceSns


with Diagram("Graph7", show=True, outformat="png", direction="TB"):

    with Cluster("Azure AD"):
        with Cluster("Mobile App Authentication Domain"):
            genericSamlToken1 = GenericSamlToken("Application Registration")
        with Cluster("Web App Authentication Domain"):
            genericSamlToken2 = GenericSamlToken("Application Registration")
    
    with Cluster("Airports"):
        aUser = User("Officer")
        aDevice = Mobile("")

    with Cluster("Dept Offices"):
        doUser1 = User("Config Editor")
        doDevice1 = Client("")
        doUser2 = User("Analyst")
        doDevice2 = Client("")

    with Cluster("AWS"):  
        with Cluster("Mobile App System Authentication"):
            cognito1 = Cognito("Cognito Userpool")

        with Cluster("Web App System Authentication"):
            cognito2 = Cognito("Cognito Userpool")

        with Cluster("Data Collection"):
            with Cluster("Submission Stage"):
                ssS3 =S3("S3 Bucket")
            
            with Cluster("Config API - Mobile"):
                camApi = APIGateway("API Gateway")
                camLambda = Lambda("Lambda")

            with Cluster("Config Store"):
                csS3 =S3("S3 Bucket")

            with Cluster("Config API - Web"):
                cawApi = APIGateway("API Gateway")
                cawLambda = Lambda("Lambda")

            with Cluster("Config Web App"):
                cwaCloudFront = CloudFront("CloudFront")
                cwaS3 =S3("S3 Bucket")

        with Cluster("Archive"):
            with Cluster("Analyst Web App"):
                awaCloudFront = CloudFront("CloudFront")
                awaS3 =S3("S3 Bucket")

        with Cluster("Data Management"):
            with Cluster("AV Scanning"):
                asSQS = SQS("SQS Queue")
                asECS = ECS("ECS Container")

            with Cluster("Data Validation"):
                dvSQS = SQS("SQS Queue")
                dvECS = ECS("ECS Container")

            with Cluster("Data Quarantine"):
                dqS3 =S3("S3 Bucket")
                sns = SimpleNotificationServiceSns("SNS Notification")
                #couldn't find icons
                snsEmail1 = Blank("")
                snsEmail2 = Blank("")


            with Cluster("Data Archive"):
                daS3 =S3("S3 Bucket")

            with Cluster("Data Archiving"):
                daECS = ECS("ECS Container")
                #couldn't find icon
                daScheEvent = Blank("Scheduled Event")

            
            

    #format within Airports
    aUser - Edge(color="red", style="invis") - aDevice
    #format within Dept Offices
    doUser1 - Edge(color="transparent") - doDevice1
    doUser2 - Edge(color="transparent") - doDevice2
    #format within Data Collection 
    camApi - Edge(color="transparent") - camLambda
    cawApi - Edge(color="transparent") - cawLambda
    cwaCloudFront - Edge(color="transparent") - cwaS3
    #format within Archive
    awaCloudFront - Edge(color="transparent") - awaS3
    #format within Data Management
    asSQS - Edge(color="transparent") - asECS
    dvSQS - Edge(color="transparent") - dvECS
    daECS - Edge(color="transparent") - daScheEvent

    #connect between sections
    #red: Data Submission
    genericSamlToken1 >> Edge(color = "#C00000", label= "Users Authenticate") << cognito1
    aDevice >> Edge(color = "#C00000", label= "Officer creates submission") >> ssS3
    aDevice >> Edge(color = "#C00000", label= "App gets config") >> camApi

    #yellow: Config Management
    genericSamlToken2 >> Edge(color = "#FFC000") << cognito2
    doDevice1 >> Edge(color = "#FFC000", label= "Config editor updates config") >> cawApi

    #dark blue: Data Analysis
    genericSamlToken2 >> Edge(color = "#2F5597", label= "Users Authenticate") << cognito2
    doDevice2 >> Edge(color = "#2F5597", label= "Analyst gets archive data") >> daS3

    #green: Data Processing
    asSQS >> Edge(color = "#70AD47", label= "Users Authenticate") >> ssS3
    asECS >> Edge(color = "#70AD47", label= "If Ok Av scanner \n sends to validation", style= "dashed") >> dvECS
    asECS >> Edge(color = "#70AD47", label= "If AV scan fails \n Data sent to Quarantine", style= "dashed") >> dqS3
    dqS3 >> Edge(color = "#70AD47", label= "Alerts security \n teams to new \n quarantine entry") >> sns
    dvECS >> Edge(color = "#70AD47", label= "Data validated and \n routed to folder in archive") >> daS3
    daScheEvent >> Edge(color = "#70AD47") >> daECS >> Edge(color = "#70AD47", label= "Scheduled Archiving creates data bundles") >> daS3
