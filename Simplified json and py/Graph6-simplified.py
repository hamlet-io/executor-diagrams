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

with Diagram("Graph6-simplified", show=True, outformat="png"):
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
    gsServer >> Edge() << jsECS
    jcpELB >> Edge() >> jsECS
    jsECS >> Edge() << jawECS2
    jawECS3 >> Edge() >> aaCloud
    codeRepo >> Edge() >> jsECS
    adUser >> Edge() >> codeRepo
    adUser >> Edge() >> genericSamlToken
    adUser >> Edge() >> jcpELB
    adUser >> Edge() >> semELB
    ses >> Edge() >> adUser
    aaDpA >> Edge() >> rcECS1