from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.generic.storage import Storage
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
from diagrams.aws.network import CloudMap
from diagrams.aws.integration import ConsoleMobileApplication

with Diagram("Graph6", show=True, outformat="png"):
#STEP1:set up groups and entities
    with Cluster("GoSource"):
        gsIamUser = IdentityAndAccessManagementIamAWSSts("AWS IAM User")
        gsServer = TradicionalServer("MacOS Build Server")

    with Cluster("Internet"):
        with Cluster("Github"):
            genericSamlToken = GenericSamlToken("oAuth Authentication Provider")
            codeRepo = Storage("Code Repositories")
        with Cluster("Application Developers"):
            adUser = User(" ")

    with Cluster("AWS Cloud"):  

        with Cluster("Jenkins CI/CD Pipeline"):
            jcpELB = ElasticLoadBalancing("Load Balancer")
            with Cluster("Jenkins Service"):
                jsECS = ECS("ECS Container")
            with Cluster("Jenkins Agent Workers"):
                jawECS1 = ECS("ECS Container")
                jawECS2 = ECS("ECS Container")
                jawECS3 = ECS("ECS Container")
            with Cluster("Shared Storage"):
                ssEFS = ElasticFileSystemEFS("EFS FileSystem")

        with Cluster("Product Accounts"):
            with Cluster("AWS Account"):
                aaCloud = Cloudformation("CloudFormation")
                aaCli = CommandLineInterface("AWS Cli")
                aaDpA = ConsoleMobileApplication("Deployed Application")

        with Cluster("Sentry Exception Monitoring"):
            semELB = ElasticLoadBalancing("Load Balancer")
            with Cluster("Sentry Application Services"):
                sasECS1 = ECS("ECS Container")
                sasECS2 = ECS("ECS Container")
                sasECS3 = ECS("ECS Container")
                ses = SimpleEmailServiceSes("SES Email")
            with Cluster("Redis Cache"):
                rcECS1 = ECS("ECS Container")
                rcCloudmap = CloudMap("AWS CloudMap")
            with Cluster("Sentry Artifact Store"):
                s3 = S3("S3 Bucket")
            with Cluster("Sentry Database"):
                sdRDS = RDS("Relational Database Service for Postgres")
            


#STEP2:set up relationships
    #format entities within one group
    gsIamUser - Edge(color="transparent") - gsServer
    genericSamlToken - Edge(color="transparent") - codeRepo
    aaCloud - Edge(color="transparent") - aaCli
    ses - Edge(color="transparent") - sasECS1
    sasECS2 - Edge(color="transparent") - sasECS3
    sasECS1 - Edge(color="transparent") - rcECS1 - Edge(color="transparent") - s3 - Edge(color="transparent") - sdRDS

    #connect between entities
    #orange: Jenkins CI/CD
    gsServer >> Edge(color = "#C55A11", label= "If the code is for a mobile app \n the build is performed on \n Apple MacOS build service") << jsECS
    jcpELB >> Edge(color = "#C55A11") >> jsECS
    jsECS >> Edge(color = "#C55A11", label= "Jenkins provisions a \n worker to build, \n test code") << jawECS2
    #jsECS >> Edge() << jawECS2

    jawECS3 >> Edge(color = "#C55A11", label= "Worker agent \n deploys code to \n product accounts") >> aaCloud
    codeRepo >> Edge(color = "#C55A11", label= "Github Notifies \n Jenkins of code change") >> jsECS
    adUser >> Edge(color = "#C55A11", label= "Developer Commits code to \n a Source code Repository") >> codeRepo
    #yellow: Developer Consoles
    adUser >> Edge(color = "#FFC000") >> genericSamlToken
    adUser >> Edge(color = "#FFC000") >> jcpELB
    adUser >> Edge(color = "#FFC000", label= "Developers Access consoles \n using Github Auth") >> semELB
    #blue: Sentry Reporting
    ses >> Edge(color = "#00B0F0", label= "Sentry Emails or sends slack \n messages to developers") >> adUser
    aaDpA >> Edge(color = "#00B0F0", label= "Applications report \n exceptions to sentry") >> rcECS1