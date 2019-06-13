

def test_add_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    # Should provide the following to addq_to_assignment
    # -- assignment (an integer)
    # -- question == div_id
    # -- points
    # -- autograde  one of ['manual', 'all_or_nothing', 'pct_correct', 'interact']
    # -- which_to_grade one of ['first_answer', 'last_answer', 'best_answer']
    # -- reading_assignment (boolean, true if it's a page to visit rather than a directive to interact with)
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    print(my_ass.questions())
    db = runestone_db_tools.db
    my_ass.save_assignment()
    res = db(db.assignments.name == 'test_assignment').select().first()
    assert res.description == my_ass.description
    assert str(res.duedate.date()) == str(my_ass.due.date())
    my_ass.autograde()
    my_ass.calculate_totals()
    my_ass.release_grades()
    res = db(db.assignments.id == my_ass.assignment_id).select().first()
    assert res.released == True


def test_choose_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    my_ass.description = 'Test Assignment Description'
    my_ass.make_visible()
    test_user_1.login()
    test_client.validate('assignments/chooseAssignment.html','Test Assignment Description')

def test_do_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    my_ass.description = 'Test Assignment Description'
    my_ass.make_visible()
    test_user_1.login()
    # This assignment has the fill in the blank for may had a |blank| lamb
    test_client.validate('assignments/doAssignment.html', 'Mary had a',
        data=dict(assignment_id=my_ass.assignment_id))

