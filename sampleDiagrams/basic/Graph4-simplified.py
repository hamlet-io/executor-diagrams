from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.onprem.client import Client, User
# aws resources
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.storage import S3
from diagrams.aws.general import TradicionalServer, GenericSamlToken
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.storage import EBS

with Diagram("Graph4-simplified", show=True, outformat="png"):
    #STEP1:set up groups and entities
    with Cluster("Internet"):
        with Cluster("Trusted External Parties"):
            tepUser = User("")
            tepDevice = Client("")

    with Cluster("Dept"):
        with Cluster("Department Staff"):
            dsUser = User("")
            dsDevice = Client("")
        with Cluster("Department SAML SSO"):
            tradicionalServer = TradicionalServer("")
            genericSamlToken = GenericSamlToken("")

    with Cluster("AWS Cloud"):
        simpleEmailServiceSes = SimpleEmailServiceSes("Simple Email Service")

        with Cluster("Jira"):
            jELB = ElasticLoadBalancing("Load Balancer")
            jEC2 = EC2("EC2 Instance")
            jEBS = EBS("EBS Volume")
            jRDS = RDS("Relational Database Service for Postgres")

        with Cluster("Confluence"):
            cELB = ElasticLoadBalancing("Load Balancer")
            cECS = ECS("EC2 Instance")
            cEBS = EBS("EBS Volume")
            cRDS = RDS("Relational Database Service for Postgres")

    #STEP2:set up relationships
    dsDevice >> Edge() >> tradicionalServer
    dsDevice >> Edge() >> genericSamlToken
    jELB >> Edge() >> jEC2
    jEC2 >> Edge() >> jRDS
    jEC2 >> Edge() >> jEBS
    cELB >> Edge() >> cRDS
    cECS >> Edge() >> cEBS
    jEC2 >> Edge() >> simpleEmailServiceSes 
    cECS >> Edge() >> simpleEmailServiceSes
    tepDevice >> Edge() >> jELB
    tepDevice >> Edge() >> cELB
    dsDevice >> Edge() >> jELB
    dsDevice >> Edge() >> cELB