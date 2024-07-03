def move_claw(current_position, target_position, actions):
    while current_position < target_position:
        actions.append("RIGHT")
        current_position += 1
    while current_position > target_position:
        actions.append("LEFT")
        current_position -= 1
    return current_position


def grab_box(box_held, actions):
    if not box_held:
        actions.append("PICK")
        box_held = 1
    return box_held


def drop_box(box_held, actions):
    if box_held:
        actions.append("PLACE")
        box_held = 0
        return box_held


def balance_stacks(claw_position, stacks, box_held, target_height, actions):
    stack_count = len(stacks)
    for i in range(stack_count):
        while stacks[i] > target_height:
            if len(actions) >= 100:
                return claw_position, box_held, True  # Exceeded command limit
            claw_position = move_claw(claw_position, i, actions)
            box_held = grab_box(box_held, actions)
            for j in range(stack_count):
                if stacks[j] < target_height:
                    claw_position = move_claw(claw_position, j, actions)
                    box_held = drop_box(box_held, actions)
                    stacks[i] -= 1
                    stacks[j] += 1
                    if stacks[j] > 5:
                        return claw_position, box_held, True
                    break
        return claw_position, box_held, False


def distribute_remainder(claw_position, stacks, box_held, target_height, extra_boxes, actions):
    stack_count = len(stacks)
    for i in range(stack_count):
        if extra_boxes == 0:
            break
        if stacks[i] < target_height + 1:
            if len(actions) >= 100:
                return claw_position, box_held, True
            claw_position = move_claw(claw_position, i, actions)
            if not box_held:
                for j in range(stack_count):
                    if stacks[j] > target_height:
                        claw_position = move_claw(claw_position, j, actions)
                        box_held = grab_box(box_held, actions)
                        stacks[j] -= 1
                        break
            box_held = drop_box(box_held, actions)
            stacks[i] += 1
            extra_boxes -= 1
            if stacks[i] > 5:
                return claw_position, box_held, True
    return claw_position, box_held, False


def solve(claw_position, boxes, box_in_claw):
    stack_count = len(boxes)
    total_boxes = sum(boxes)
    target_height = total_boxes // stack_count
    extra_boxes = total_boxes % stack_count

    actions = []

    claw_position, box_in_claw, limit_exceeded = balance_stacks(claw_position, boxes, box_in_claw, target_height, actions)
    if limit_exceeded:
        return ["WARNING"]

    claw_position, box_in_claw, limit_exceeded = distribute_remainder(claw_position, boxes, box_in_claw, target_height,
                                                                   extra_boxes, actions)
    if limit_exceeded:
        return ["WARNING"]

    if len(actions) > 100:
        return "YOU LOST"

    return actions


