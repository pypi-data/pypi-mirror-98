import time
from funcx.tests.fn_module import imported_fn


def local_fn():
    return True


def test_imported_function(fxc, endpoint):

    fn_uuid = fxc.register_function(imported_fn, endpoint, description='platinfo')
    task_id = fxc.run(endpoint_id=endpoint,
                      function_id=fn_uuid)

    print("Task_id: ", task_id)

    for i in range(5):
        try:
            r = fxc.get_result(task_id)
            print(f"result : {r}")
        except Exception:
            time.sleep(2)
        else:
            break


def test_local_function(fxc, endpoint):

    fn_uuid = fxc.register_function(local_fn, endpoint, description='local_fn')
    task_id = fxc.run(endpoint_id=endpoint,
                      function_id=fn_uuid)

    print("Task_id: ", task_id)

    for i in range(5):
        try:
            r = fxc.get_result(task_id)
            print(f"result : {r}")
        except Exception:
            time.sleep(2)
        else:
            break


def test_nested_scope_function(fxc, endpoint):

    def in_scope_fn():
        return False

    fn_uuid = fxc.register_function(in_scope_fn, endpoint, description='in_scope_fn')
    task_id = fxc.run(endpoint_id=endpoint,
                      function_id=fn_uuid)

    print("Task_id: ", task_id)

    for i in range(5):
        try:
            r = fxc.get_result(task_id)
            print(f"result : {r}")
        except Exception:
            time.sleep(2)
        else:
            break
