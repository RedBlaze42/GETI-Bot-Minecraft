# coding: utf8

def getToken():
    with open("token.secret","r") as tokenFile:
        return tokenFile.read().split("\n")[0]

async def getRole(client,guild,role_name,create_if_not_created=True):
    for role in guild.roles:
        if role.name==role_name:
            return role
    if create_if_not_created:
        created_role = await guild.create_role(name=role_name,mentionable=True)
        await guild.owner.send("J'ai créé le role "+role_name+" car j'en ai besoin et il n'existait pas")
        return created_role