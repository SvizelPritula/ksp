use std::io::{stdin, BufRead};

use anyhow::{anyhow, bail, Result};
use solve::{get_min_changes, Node, Pipe};

mod solve;

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
struct GraphPipe {
    pub open: bool,
    pub node: usize,
}

#[derive(Debug, Clone, Hash)]
struct GraphNode {
    sink: Option<bool>,
    neighbours: Vec<GraphPipe>,
}

fn build_tree(nodes: &Vec<GraphNode>, root: usize, parent: Option<usize>) -> Node {
    let node = &nodes[root];

    match node.sink {
        Some(target_flow) => Node::Sink { target_flow },
        None => {
            let pipes = node
                .neighbours
                .iter()
                .copied()
                .filter(|pipe| Some(pipe.node) != parent)
                .map(|GraphPipe { open, node }| Pipe {
                    node: build_tree(nodes, node, Some(root)),
                    open,
                })
                .collect();

            Node::Switch { pipes }
        }
    }
}

fn main() -> Result<()> {
    let input = stdin().lock();
    let mut lines = input.lines();

    let [node_count, sink_count]: [usize; 2] = lines
        .next()
        .ok_or_else(|| anyhow!("unexpected EOF"))??
        .split_whitespace()
        .map(|t| t.parse())
        .collect::<Result<Vec<_>, _>>()?
        .try_into()
        .map_err(|_| anyhow!("expected two elements in header"))?;

    if node_count == 0 {
        bail!("expected at least one node")
    }

    let mut nodes = vec![
        GraphNode {
            neighbours: Vec::new(),
            sink: None
        };
        node_count
    ];

    for _ in 0..(node_count - 1) {
        let pipe = lines.next().ok_or_else(|| anyhow!("unexpected EOF"))??;

        let [from, to, open]: [&str; 3] = pipe
            .split_whitespace()
            .collect::<Vec<_>>()
            .try_into()
            .map_err(|_| anyhow!("expected three elements in tube description"))?;

        let from: usize = from.parse()?;
        let to: usize = to.parse()?;

        if from == 0 || to == 0 {
            bail!("node id cannot be zero");
        }

        let open = match open.parse()? {
            'O' => Ok(true),
            'Z' => Ok(false),
            c => Err(anyhow!("unknown open state {c}")),
        }?;

        nodes
            .get_mut(from - 1)
            .ok_or_else(|| anyhow!("unknown node {from}"))?
            .neighbours
            .push(GraphPipe { open, node: to - 1 });

        nodes
            .get_mut(to - 1)
            .ok_or_else(|| anyhow!("unknown node {to}"))?
            .neighbours
            .push(GraphPipe { open, node: from - 1 });
    }

    for _ in 0..sink_count {
        let sink = lines.next().ok_or_else(|| anyhow!("unexpected EOF"))??;

        let [id, target_flow]: [&str; 2] =
            sink.split_whitespace()
                .collect::<Vec<_>>()
                .try_into()
                .map_err(|_| anyhow!("expected two elements in sink description"))?;

        let id: usize = id.parse()?;

        if id == 0 {
            bail!("node id cannot be zero");
        }

        let target_flow = match target_flow.parse()? {
            'P' => Ok(Some(true)),
            'M' => Ok(Some(false)),
            'E' => Ok(None),
            c => Err(anyhow!("unknown target flow {c}")),
        }?;

        let node = nodes
            .get_mut(id - 1)
            .ok_or_else(|| anyhow!("unknown node {id}"))?;

        if let Some(target_flow) = target_flow {
            if node.neighbours.len() > 1 {
                bail!("a sink must be a leaf");
            }

            if node.sink.is_some() {
                bail!("only one sink type is allowed per node");
            }

            node.sink = Some(target_flow);
        }
    }

    let root = build_tree(&nodes, 0, None);
    let changes = get_min_changes(root);

    println!("{changes}");

    Ok(())
}
