pub struct Pipe {
    pub open: bool,
    pub node: Node,
}

pub enum Node {
    Sink { target_flow: bool },
    Switch { pipes: Vec<Pipe> },
}

fn get_min_changes_impl(root: Node) -> (usize, Option<bool>) {
    match root {
        Node::Sink { target_flow } => (0, Some(target_flow)),
        Node::Switch { pipes } => {
            let mut changes = 0;

            let mut need_flow = 0usize;
            let mut need_no_flow = 0usize;

            for Pipe { open, node } in pipes {
                let (pipe_changes, target_flow) = get_min_changes_impl(node);

                changes += pipe_changes;

                match target_flow {
                    Some(true) => {
                        need_flow += 1;

                        if !open {
                            changes += 1;
                        }
                    }
                    Some(false) => {

                        if open {
                            need_no_flow += 1;
                        }
                    }
                    None => {}
                }
            }

            let target_flow = match (need_flow > 0, need_no_flow > 0) {
                (true, _) => {
                    changes += need_no_flow;
                    Some(true)
                }
                (false, true) => Some(false),
                (false, false) => None,
            };

            (changes, target_flow)
        }
    }
}

pub fn get_min_changes(root: Node) -> usize {
    match root {
        Node::Sink { target_flow: _ } => 0,
        Node::Switch { pipes } => {
            let mut changes = 0;

            for Pipe { open, node } in pipes {
                let (pipe_changes, target_flow) = get_min_changes_impl(node);

                changes += pipe_changes;

                if let Some(target_flow) = target_flow {
                    if target_flow != open {
                        changes += 1;
                    }
                }
            }

            changes
        }
    }
}
