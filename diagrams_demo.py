import json
import click
from jinja2 import Template


#create group object to represent Cluster
class group(object):
    def __init__(self,dit):
        self.parentID = dit['parentID']
        self.groupID = dit['groupID']
        self.childIDs = []
        self.entities = []
        self.template = ''
        self.entityStr = ''
        self.rank = 0 #the rank of groups increment as it goes deeper
        self.libraries = []

    #find child groups for parent groups, store childIDs for group object
    def findChildGroups(self,groups):
        for group in groups:
            if group.parentID == self.groupID and group != self:
                self.childIDs.append(group)

    #find entities of each group, store entities for group object
    def findEntities(self,entitiesGroup):
        for en in entitiesGroup:
            if en['groupID'] == self.groupID:
                self.libraries.append(en['type']) #save for library import
                en['type'] = en['type'].rsplit('.')[-3] + '_' + en['type'].rsplit('.')[-2] + '.' + en['type'].split('.')[-1]
                self.entities.append(en)

    #create Cluster template
    def createCluster(self):
        template =Template("""\
                with Cluster("{{groupID}}"):
                    {% for entity in entities %}
                    {{entity.entityID}}={{entity.type}}("{{entity.entityName}}")
                    {% endfor %}
            """).render(groupID=self.groupID,entities=self.entities)
        self.entityStr = template
        self.template = template
        return self.template

#main function, input json file path and template file path
@click.command()
@click.option('--json-path', type=click.Path(exists=True, file_okay=True, readable=True), required=True, help='The exec format document')
@click.option('--temp-path', type=click.Path(file_okay=True, writable=True ), required=True, help='The template output file')
def main(json_path,temp_path=r'template.py'):
    #parse json file and get diagramName, groups, entities and relationships store as dict or list
    with open(json_path, 'r', encoding='utf-8') as f:
        dictJson = json.load(f)
        for key in dictJson.keys():
            if key == 'diagramName':
                diagramName=dictJson[key]
            elif key == "groups":
                groups = dictJson[key]
            elif key == "entities":
                entities = dictJson[key]
            elif key == 'relationships':
                relationships = dictJson[key]

    #build all group objects and store in list
    #create list of group objects, array in json is list in python
    groupObjects = [0]*len(groups) #it has the length of group list
    for i in range(len(groups)):
        groupObjects[i] = group(groups[i])
    #find entities for each group and store
    for groupObj in groupObjects:
        groupObj.findEntities(entities)

    #match rank for each group and store
    rank_list =[]
    #recursion
    def matchRank(groupObjects):
        allobjects = groupObjects.copy()
        if rank_list==[]:
            for obj in groupObjects:
                #identify and remove groups with no parent
                if obj.parentID == '':
                    obj.rank = 1
                    rank_list.append(obj)
                    allobjects.remove(obj)
            groupObjects = allobjects
            matchRank(groupObjects)
        else:
            if allobjects != []: #there are still objs unmatched
                for pa_obj in rank_list:
                    for obj in groupObjects:
                        if pa_obj.groupID == obj.parentID:
                            obj.rank = pa_obj.rank+1
                            rank_list.append(obj)
                            allobjects.remove(obj)
                groupObjects = allobjects
                matchRank(groupObjects)
            else:
                return rank_list
    matchRank(groupObjects)

    #find child groups for each group and create template
    childGroups = []
    for groupObj in groupObjects:
        groupObj.findChildGroups(groupObjects) #childIDs list is populated
        groupObj.createCluster()
        if groupObj.childIDs == []: #if this group object has no child groups, save it as its own child group???
            childGroups.append(groupObj)

    #remove duplicates
    def removeDuplicates(list):
        new_list = []
        for li in list:
            if li not in new_list:
                new_list.append(li)
        return new_list

    #find parent group for each child group and combine Clusters
    def findParents(childGroups,allObjects,rootGroups):
        parentIDs = []
        for child in childGroups:
            if child.parentID == '':
                rootGroups.append(child)
            else:
                parentIDs.append(child.parentID)
        if parentIDs == []:
            return 'all groups are root groups', removeDuplicates(rootGroups)
        parentIDs = removeDuplicates(parentIDs)

        parentsList = []
        for parent in parentIDs:
            template = Template("""\n
            with Cluster("{{parentID}}"):
                {% for child in childGroups %}
                {% if child.parentID == parentID %}
                {{child.template}}
                {% endif %}
                {% endfor %}
            """).render(parentID=parent,childGroups=childGroups)
            for obj in allObjects:
                if obj.groupID == parent:
                    obj.template =obj.template + template
                    parentsList.append(obj)

        return findParents(parentsList,allObjects,rootGroups), removeDuplicates(rootGroups)

    #write all parent groups into template file
    with open(temp_path, 'w+', encoding='utf-8') as f:
        for g in findParents(childGroups,groupObjects,[])[1]:
            f.write(g.template)

    #retrive parent groups file and remove redundant spaces. (Jinja2 template generates lots of spaces and empty lines)
    with open(temp_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l !='']

    #insert remaining entities if there are any
    for obj in groupObjects:
        if obj.entities!=[] and obj.childIDs!=[]:
            str = "with Cluster(\"{}\"):".format(obj.groupID)
            lines = [obj.entityStr if l==str else l for l in lines]

    #write template in file
    with open(temp_path, 'w+', encoding='utf-8') as f:
        for l in lines:
            f.write(l+'\n')

    #remove redundant spaces and empty lines
    with open(temp_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l != '']
        lines = removeDuplicates(lines)

        #get group rank for Cluster
        def clusterRank(str):
            name = str.split('"')[1].split('"')[0]
            for obj in groupObjects:
                if obj.groupID == name:
                    return obj.rank

        #import libraries from entity types
        import_diagrams = "import diagrams\nfrom diagrams import Cluster, Diagram, Edge\nfrom diagrams.generic.blank import Blank\n"
        imported_libraries = []
        for obj in groupObjects:
            for diagClass in obj.libraries:
                import_module = diagClass.rsplit('.', 1)[0]
                if import_module not in imported_libraries:
                    imported_libraries.append(import_module)
                    import_name = diagClass.rsplit('.')[1] + '_' + diagClass.rsplit('.')[2]
                    import_command = f'import {import_module} as {import_name} \n'
                    import_diagrams = import_diagrams + import_command

        exe_temp=import_diagrams + '\nwith Diagram(\"{}\", show=False, outformat="png", direction="TB"):\n'.format(diagramName)
        space ='    ' #indent
        rank = 0
        for i in range(len(lines)):
            if 'with' in lines[i]:
                rank = clusterRank(lines[i])
                lines[i] = space*rank+lines[i]+'\n' #indent according to ranks
            else:
                if 'with' in lines[i-1]:
                    rank = rank+1
                lines[i] = space * rank + lines[i]+'\n'
            exe_temp = exe_temp+lines[i]

    #add relationships
    for rela in relationships:
        if isinstance(rela,dict):
            if rela['direction'] == 'one way':
                rela_str = space + rela['startEntityID'] +' '+'>>'+' '+'Edge()'+' '+'>>'+' '+rela['endEntityID']+'\n'
                exe_temp = exe_temp + rela_str
            elif rela['direction'] == 'two way':
                rela_str = space + rela['startEntityID'] + ' ' + '>>'+' ' + 'Edge()' + ' ' + '<<' + ' ' + rela['endEntityID'] + '\n'
                exe_temp = exe_temp + rela_str

    #write exe template into file for checking
    f = open(temp_path, 'w+', encoding='utf-8')
    f.write(exe_temp)
    f.close()

    #run template file and see results
    exec(exe_temp)

#specify the json file path here:
if __name__ == "__main__":
    #first parameter is the path for json file, second parameter is path for output template file
    main()
