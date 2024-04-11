from flask_restx import Namespace,Resource,fields

todoController = Namespace("todo", path="/todos/", description = "Todos API Controller")

todosDB = []

# Model
createTaskCommand = todoController.model("createTaskCommand",{
    'task': fields.String(required=True,description='todo details')
})

todoDto = todoController.model("todoDto",{
    'task': fields.String(required=True,description='About the Todo')
})

@todoController.route("/")
class Todos(Resource):
    @todoController.marshal_list_with(todoDto)
    def get(self):
        return todosDB
    
    @todoController.expect(createTaskCommand)
    def post(self):
        newTodo=todoController.payload
        newId= 1 if len(todosDB) == 0 else 1+max([x["id"] for x in todosDB])
        todosDB.append({"id":newId,"task":newTodo["task"]})

@todoController.route("/<int:id>")
class Todo(Resource):
    @todoController.marshal_with(todoDto)
    def get(self,id):
        desiredTodos= [x for x in todosDB if x["id"] == id]
        if len(desiredTodos) > 0:
            return desiredTodos[0]
        todoController.abort(404, f"TODO with {id} does not exist")

    @todoController.expect(todoDto)
    def put(self, id):
        TodoDbIds = [x["id"] for x in todosDB]
        if not id in TodoDbIds:
            todoController.abort(404, f"TODO with {id} does not exist")
        todoInd=[x["id"] for x in todosDB].index(id)
        todosDB[todoInd]["task"] = todoController.payload["task"]
        return todosDB[todoInd]
    
    def delete(self,id):
        global todosDB
        TodoDbIds = [x["id"] for x in todosDB]
        if id not in TodoDbIds:
            todoController.abort(404, f"TODO with {id} does not exist")
        todosDB = [x for x in todosDB if x["id"] != id]
        return '',204
