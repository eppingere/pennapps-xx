import boto3
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')


# insurers_table.delete()
# hospitals_table.delete()

# Create the DynamoDB table.
# hospitals_table = dynamodb.create_table(
#     TableName='hospitals',
#     KeySchema=[
#         {
#             'AttributeName': 'name',
#             'KeyType': 'HASH'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'name',
#             'AttributeType': 'S'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )


# Create the DynamoDB table.
# insurers_table = dynamodb.create_table(
#     TableName='insurers',
#     KeySchema=[
#         {
#             'AttributeName': 'name',
#             'KeyType': 'HASH'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'name',
#             'AttributeType': 'S'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# # # Wait until the table exists.
insurers_table = dynamodb.Table('insurers')
hospitals_table = dynamodb.Table('hospitals')


# insurers_table = dynamodb.Table('insurers')
# hospitals_table = dynamodb.Table('hospitals')


# print(insurers_table.creation_date_time)
# print(hospitals_table.creation_date_time)

with insurers_table.batch_writer() as batch:
    batch.put_item(
       Item={
            #'uid':'uhg',
            'name': 'UnitedHealthcare Group',
            'copay': '40',
        }
    )

    batch.put_item(
       Item={
            #'uid':'kfg',
            'name': 'Kaiser Foundation Group',
            'copay': '50',
        }
    )

    batch.put_item(
       Item={
            #'uid':'ag',
            'name': 'Aetna Group',
            'copay': '40',
        }
    )

    batch.put_item(
       Item={
            #'uid':'chg',
            'name': 'Cigna Health Group',
            'copay': '50',
        }
    )

    batch.put_item(
       Item={
            #'uid':'bcbs',
            'name': 'Blue Cross Blue Shield Group',
            'copay': '30',
        }
    )
with hospitals_table.batch_writer() as batch:
    batch.put_item(
       Item={
            #'uid':'kfg',
            'name': 'Massachusetts General Hospital',
            'address':'55 Fruit Street, Boston, MA 02114',
            'phone': '(617)-726-2000',
            'accepted_insurance':'UnitedHealthcare Group',
            'waittime':0,
        }
    )

    batch.put_item(
       Item={
            #'uid':'bwh',
            'name': 'Brigham and Women\'s Hospital',
            'address':'75 Francis Street, Boston, MA 02115',
            'phone': '(617)-732-5500',
            'accepted_insurance':'Aetna Group',
            'waittime':0,
        }
    )

    batch.put_item(
       Item={
            'name': 'Boston Medical Center',
            'address':'One Boston Medical Center Place, Boston, MA 02118',
            'phone': '(617)-414-4075',
            'accepted_insurance':'Blue Cross Blue Shield Group',
            'waittime':0,
        }
    )

    batch.put_item(
       Item={
            'name': 'Tufts Medical Center',
            'address':'800 Washington St, Boston, MA 02111',
            'phone': '(617)-636-5000',
            'accepted_insurance':'Kaiser Foundation Group',
            'waittime':0,
        }
    )

# response = dynamodb.scan(
#     TableName='string',
#     IndexName='string',
#     AttributesToGet=[
#         'name',
#     ])
# item = response['Item']
# print(item)

response = hospitals_table.query(
    KeyConditionExpression=Key('name').eq('Tufts Medical Center')
)

for i in response['Items']:
    print(i['name'], ":", i['address'], ":", i['phone'], ":", i['accepted_insurance'])