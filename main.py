import pandas as pd
import boto3
from boto3.session import Session
import vpc_service, subnet_service, route_service, vpn_service, nat_service
import security_service, ec2_service, elb_service, rds_service, cloudfront_service
import s3_service, direct_connect_service
import sys


# Gathering vpc infos, name, id, cidr, flow logs
def get_vpc_info(tag_val, ec2):
    vpc = vpc_service.vpc(ec2)
    get_vpc = vpc.desecribe_vpc(tag_val)

    return get_vpc


# vpc_id is list type
def get_subnet_info(vpc_id, ec2):
    subnets = subnet_service.subnet(ec2)
    get_sub_info = subnets.describe_subnet(vpc_id)

    return get_sub_info


# subnet_id is list type
def get_route_info(subnet_id, ec2):
    routes = route_service.route(ec2)
    get_route_info = routes.describe_route(subnet_id)

    return get_route_info


# vpc_id is list type
def get_vpn_info(vpc_id, ec2):
    vpn = vpn_service.vpn(ec2)
    get_vpn_info = vpn.describe_vpn_gates(vpc_id)

    return get_vpn_info


# vpc_id is list type
def get_nat_info(vpc_id, ec2):
    nat = nat_service.nat(ec2)
    get_nat_info = nat.describe_nats(vpc_id)

    return get_nat_info


def get_securities_info(vpc_id, ec2):
    securities = security_service.security_groups(ec2)
    get_securities_info = securities.describe_ips(vpc_id)

    return get_securities_info


def get_instances_info(vpc_id, ec2):
    instances = ec2_service.ec2(ec2)
    get_ec2_info = instances.get_instance_ids(vpc_id)

    return get_ec2_info


def get_elbs_info(elb, elbv2):
    elbs = elb_service.elb(elb, elbv2)
    get_classic_elb_info = elbs.descrbie_classic_elb()
    get_not_classic_elb_info = elbs.describe_not_classic_elb()

    result = get_classic_elb_info+get_not_classic_elb_info

    return result


def get_rds_info(rds):
    rdss = rds_service.rds(rds)
    get_rds_info = rdss.get_db_arn()

    return get_rds_info


def get_cf_info(cf):
    cfs = cloudfront_service.cloudfront(cf)
    get_cfs_info = cfs.describe_cfs()

    return get_cfs_info


def get_s3_info(s3):
    s3s = s3_service.s3s(s3)
    get_s3s_info = s3s.describe_s3s()

    return get_s3s_info


def get_dx_info(direct):
    direct = direct_connect_service.direct_connect(direct)
    get_direct_connection = direct.describe_dx()

    return get_direct_connection

if __name__ == '__main__':
    print('Console to xlsx started')

    # basic environment setting
    region = sys.argv[1]
    profile_name = sys.argv[2]

    if profile_name != '':
        session = Session(profile_name=profile_name, region_name=region)
        ec2 = session.client('ec2', region_name=region)
        direct_connect = session.client('directconnect', region_name=region)
        elb = session.client('elb', region_name=region)
        elbv2 = session.client('elbv2')
        rds = session.client('rds', region_name=region)
        cf = session.client('cloudfront')
        s3 = session.client('s3')
        direct = session.client('directconnect')
    else:
        ec2 = boto3.client('ec2', region_name=region)
        direct_connect = boto3.client('directconnect', region_name=region)
        elb = boto3.client('elb', region_name=region)
        elbv2 = boto3.client('elbv2')
        rds = boto3.client('rds', region_name=region)
        cf = boto3.client('cloudfront')
        s3 = boto3.client('s3')
        direct = boto3.client('directconnect')

    xlsx_name = sys.argv[3]
    writer_vpc_info = pd.ExcelWriter(xlsx_name, engine='xlsxwriter')
    workbook = writer_vpc_info.book
    start_row = 3

    #format to apply to xlsx
    border_format = workbook.add_format({'border': 1})

    # get vpc info
    tag_val = ['api_private_test']
    vpc_labels = ['Name', 'ID', 'CIDR', 'Flow Logs']
    vpc_values = get_vpc_info(tag_val, ec2)
    df_vpc = pd.DataFrame.from_records(vpc_values, columns=vpc_labels)
    df_vpc.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=3)
    worksheet = writer_vpc_info.sheets['4.VPC 구성정보']
    worksheet.write(0, 0, '2. VPC 구성정보')
    worksheet.write(2, 0, '2.1 VPC 현황')
    worksheet.write(start_row, 0, '연번', border_format)
    start_row += len(df_vpc)+3
    print('vpc info', len(df_vpc), df_vpc)

    # get subnet info
    vpc_ids = []
    for name, _, vpc_id, _ in vpc_values:
        vpc_ids.append(vpc_id)

    subnet_labels = ['Name', 'ID', 'VPC', 'CIDR', 'Route Table']
    sub_values = get_subnet_info(vpc_ids, ec2)
    df_subnet = pd.DataFrame.from_records(sub_values, columns=subnet_labels)
    df_subnet.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row-1, 0, '2.2 Subnet 현황')
    worksheet.write(start_row, 0, '연번')
    start_row += len(df_subnet)+3
    print('sub info', df_subnet)

    # get route info
    sub_ids = []
    for _, subid, _, _, _ in sub_values:
        sub_ids.append(subid)

    route_labels = ['Name', 'Route Table ID', 'Main']
    route_values = get_route_info(sub_ids, ec2)
    df_route = pd.DataFrame.from_records(route_values, columns=route_labels)
    df_route.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row-1, 0, '2.3 Route Table 현황')
    worksheet.write(start_row, 0, '연번')
    start_row += len(df_route)+3
    print('route info', df_route)

    # get vpn info
    vpn_values = None
    vpn_labels = ['Name', 'CGW ID', 'VPN ID', 'Custome IP', '장비 정보', 'Tunnel1', 'Tunnel2', 'Static Routes', 'Etc']
    for vid in vpc_ids:
        vpn_values = get_vpn_info(vid, ec2)
    df_vpn = pd.DataFrame.from_records(vpn_values, columns=vpn_labels)
    df_vpn.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row-1, 0, '2.4 VPN 현황')
    worksheet.write(start_row, 0, '연번')
    start_row += len(df_vpn)+3
    print('vpn info', vpn_values)

    # get nat info
    nat_values = None
    nat_labels = ['ID', 'EIP', 'PIP', 'VPC', 'Subnet']
    for vid in vpc_ids:
        nat_values = get_nat_info(vid, ec2)
    df_nat = pd.DataFrame.from_records(nat_values, columns=nat_labels)
    df_nat.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row-1, 0, '2.5 NAT Gateway 현황')
    worksheet.write(start_row, 0, '연번')
    start_row += len(df_nat)+3
    print('nat info', df_nat)

    # get direct connect info
    direct_values = None
    direct_values = get_dx_info(direct)
    direct_labels = ['Name', 'ID', 'Connection', 'VGW', 'Your Peer IP', 'Amazon Peer IP']
    df_direct = pd.DataFrame.from_records(direct_values, columns=direct_labels)
    df_direct.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row-1, 0, '2.6 Direct Connect 현황')
    worksheet.write(start_row, 0, '연번')
    start_row += len(df_direct)+3
    print('DX info', df_direct)

    # get securties info
    security_values = None
    df_sg = pd.DataFrame()
    sg_labels = ['ID', 'Name', 'Type', 'Protocol', 'Port Range', 'Source', 'Description']
    for vid in vpc_ids:
        security_values = get_securities_info(vid, ec2)
    print('security info', security_values)

    for col in security_values:
        df_to_append = pd.DataFrame.from_records(col, columns=sg_labels)
        df_sg = df_sg.append(df_to_append)
    df_sg.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row-1, 0, '2.7 Security Group 현황')
    worksheet.write(start_row, 0, '연번')
    start_row += len(df_sg)+3
    print(df_sg)

    # get instance info

    instances_values = None
    ec2_start_row = 3
    df_ec2 = pd.DataFrame()
    ec2_labels = ['Name', 'Instance ID', 'Type', 'AZ', 'Key Pair', 'Security Group', 'IAM Role', 'EIP', 'PIP', 'ID', 'PW', 'EBS', 'OS', 'etc']
    for vid in vpc_ids:
        instances_values = get_instances_info(vid, ec2)
    print(instances_values)

    ec2_to_append = pd.DataFrame.from_records(instances_values, columns=ec2_labels)
    df_ec2 = df_ec2.append(ec2_to_append)
    df_ec2.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=3)
    worksheet_ec2 = writer_vpc_info.sheets['5.EC2 현황정보']
    worksheet_ec2.write(0, 0, '3. EC2 현황정보')
    worksheet_ec2.write(2, 0, '3.1 Instance 현황')
    worksheet_ec2.write(ec2_start_row, 0, '연번')
    ec2_start_row += len(df_ec2) + 3
    print(df_ec2)

    # get elbs info
    elbs_values = get_elbs_info(elb, elbv2)
    elb_labels = ['Name', 'DNS Name', 'Port', 'AZ', 'Host Count', 'Health Check']
    df_elbs = pd.DataFrame.from_records(elbs_values, columns=elb_labels)
    df_elbs.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
    worksheet_ec2.write(ec2_start_row-1, 0, '3.2 ELB 현황')
    worksheet_ec2.write(ec2_start_row, 0, '연번')
    print('elb and elbv2 info ', df_elbs)

    # get rds info
    rds_values = get_rds_info(rds)
    rds_labels = ['Name', 'DB Name', 'DB Engine', 'Type', 'Storage', 'ID', 'PW', 'Character Set', 'Multi-Az', 'Publicly', 'Endpoint']
    df_rds = pd.DataFrame.from_records(rds_values, columns=rds_labels)
    df_rds.to_excel(writer_vpc_info, sheet_name='6.RDS 현황정보', startrow=2)
    worksheet_rds = writer_vpc_info.sheets['6.RDS 현황정보']
    worksheet_rds.write(0, 0, '4.RDS 현황정보')
    worksheet_rds.write(2, 0, '연번')
    print('rds info \n', df_rds)

    # get cf info
    cfs_values = get_cf_info(cf)
    cfs_labels = ['ID', 'Domain', 'Origin', 'CNAMEs', 'Etc']
    cf_start_row = 3
    df_cfs = pd.DataFrame.from_records(cfs_values, columns=cfs_labels)
    df_cfs.to_excel(writer_vpc_info, sheet_name='7.CloudFront&S3', startrow=cf_start_row)
    worksheet_cf = writer_vpc_info.sheets['7.CloudFront&S3']
    cf_start_row += len(df_cfs)+3
    worksheet_cf.write(0, 0, 'CloudFront&S3 현황정보')
    worksheet_cf.write(2, 0, '5.1CloudFront')
    worksheet_cf.write(3, 0, '연번')
    print('cloud front info ', df_cfs)

    # get s3 info
    s3_values = get_s3_info(s3)
    s3_labels = ['Bucket Name', 'Region', 'Use', 'User', 'Authority']
    df_s3s = pd.DataFrame.from_records(s3_values, columns=s3_labels)
    df_s3s.to_excel(writer_vpc_info, sheet_name='7.CloudFront&S3', startrow=cf_start_row)
    worksheet_cf.write(cf_start_row-1, 0, '5.S3')
    worksheet_cf.write(cf_start_row, 0, '연번')
    print(df_s3s)

    # saved the xlsx
    writer_vpc_info.save()
    exit()
