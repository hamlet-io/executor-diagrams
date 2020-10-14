import diagrams
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.generic.blank import *
from diagrams.onprem.compute import *
from diagrams.generic.blank import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *

with Diagram("Graph-testing123", show=True, outformat="png", direction="TB"):
    with Cluster("apigatewaybase"):
        with Cluster("application-apigatewaybase"):
            appXapigatewaybase=Server("mockedup-integration-application-apigatewaybase")
    with Cluster("filetransferbase"):
        with Cluster("application-filetransferbase"):
            appXfiletransferbase=Server("mockedup-integration-application-filetransferbase")
    with Cluster("s3base"):
        with Cluster("application-s3base"):
            appXs3base=Server("mockedup-integration-application-s3base")
    with Cluster("postgresdbbase"):
        with Cluster("database-postgresdbbase"):
            dbXpostgresdbbase=Server("mockedup-integration-database-postgresdbbase")
    with Cluster("postgresdbgenerated"):
        with Cluster("database-postgresdbgenerated"):
            dbXpostgresdbgenerated=Server("mockedup-integration-database-postgresdbgenerated")
    with Cluster("ssh"):
        with Cluster("management-ssh"):
            mgmtXssh=Server("mockedup-integration-management-ssh")
    with Cluster("httpslb"):
        with Cluster("elb-httpslb"):
            elbXhttpslb=Server("mockedup-integration-elb-httpslb")
            with Cluster("elb-httpslb-httpredirect"):
                elbXhttpslbXhttpredirect=Server("mockedup-integration-elb-httpslb-httpredirect")
            with Cluster("elb-httpslb-https"):
                elbXhttpslbXhttps=Server("mockedup-integration-elb-httpslb-https")
    with Cluster("baseline"):
        with Cluster("management-baseline"):
            mgmtXbaseline=Server("mockedup-integration-management-baseline")
            with Cluster("management-baseline-appdata"):
                mgmtXbaselineXappdata=Server("mockedup-integration-management-baseline-appdata")
            with Cluster("management-baseline-cmk"):
                mgmtXbaselineXcmk=Server("mockedup-integration-management-baseline-cmk")
            with Cluster("management-baseline-oai"):
                mgmtXbaselineXoai=Server("mockedup-integration-management-baseline-oai")
            with Cluster("management-baseline-opsdata"):
                mgmtXbaselineXopsdata=Server("mockedup-integration-management-baseline-opsdata")
            with Cluster("management-baseline-ssh"):
                mgmtXbaselineXssh=Server("mockedup-integration-management-baseline-ssh")
    with Cluster("igw"):
        with Cluster("management-igw"):
            mgmtXigw=Server("mockedup-integration-management-igw")
            with Cluster("management-igw-default"):
                blank2=Blank("#Blank#")
    with Cluster("nat"):
        with Cluster("management-nat"):
            mgmtXnat=Server("mockedup-integration-management-nat")
            with Cluster("management-nat-default"):
                blank1=Blank("#Blank#")
    with Cluster("vpcendpoint"):
        with Cluster("management-vpcendpoint"):
            mgmtXvpcendpoint=Server("mockedup-integration-management-vpcendpoint")
            with Cluster("management-vpcendpoint-default"):
                mgmtXvpcendpointXdefault=Server("mockedup-integration-management-vpcendpoint-default")
    with Cluster("vpc"):
        with Cluster("management-vpc"):
            mgmtXvpc=Server("mockedup-integration-management-vpc")
            with Cluster("management-vpc-external"):
                mgmtXvpcXexternal=Server("mockedup-integration-management-vpc-external")
            with Cluster("management-vpc-internal"):
                mgmtXvpcXinternal=Server("mockedup-integration-management-vpc-internal")
            with Cluster("management-vpc-open"):
                mgmtXvpcXopen=Server("mockedup-integration-management-vpc-open")
