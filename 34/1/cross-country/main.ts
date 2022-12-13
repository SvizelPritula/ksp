import * as fs from "fs/promises";
import Denque from "denque";

interface Node {
  edges: Edge[];
  distance: number;
}

interface Edge {
  node: Node;
  length: number;
}

interface Crossing {
  dryNode: Node;
  wetNode: Node;
}

interface Input {
  crossings: Crossing[];
  start: Node;
  end: Node;
}

function solve(input: Input): number {
  var queue: Denque<Node> = new Denque();

  input.start.distance = 0;
  queue.push(input.start);

  while (!queue.isEmpty()) {
    var node = queue.shift();

    for (var edge of node.edges) {
      var distance = node.distance + edge.length;

      if (distance < edge.node.distance) {
        edge.node.distance = distance;
        queue.push(edge.node);
      }
    }
  }

  return input.end.distance;
}

function parseFile(string: string): Input {
  string = string.trim();

  let lines = string.split("\n").map((l) =>
    l
      .trim()
      .split(" ")
      .map((t) => parseInt(t, 10))
  );

  let [crossingCount, edgeCount, startIndex, endIndex, switchTime] = lines[0];

  let crossings: Crossing[] = [];

  for (let i = 0; i < crossingCount; i++) {
    var dryNode: Node = { edges: [], distance: Infinity };
    var wetNode: Node = { edges: [], distance: Infinity };

    dryNode.edges.push({ length: switchTime, node: wetNode });
    wetNode.edges.push({ length: switchTime, node: dryNode });

    crossings.push({ dryNode, wetNode });
  }

  for (let i = 0; i < edgeCount; i++) {
    let [startIndex, endIndex, wetTime, dryTime] = lines[i + 1];

    crossings[startIndex].dryNode.edges.push({
      length: dryTime,
      node: crossings[endIndex].dryNode,
    });

    crossings[startIndex].wetNode.edges.push({
      length: wetTime,
      node: crossings[endIndex].wetNode,
    });

    crossings[endIndex].dryNode.edges.push({
      length: dryTime,
      node: crossings[startIndex].dryNode,
    });

    crossings[endIndex].wetNode.edges.push({
      length: wetTime,
      node: crossings[startIndex].wetNode,
    });
  }

  return {
    crossings: crossings,
    start: crossings[startIndex].wetNode,
    end: crossings[endIndex].dryNode,
  };
}

async function run(input: string, output: string) {
  var inputData = await fs.readFile(input, { encoding: "utf-8" });
  var parsedData = parseFile(inputData);
  var result = solve(parsedData).toString(10);
  await fs.writeFile(output, result, { encoding: "utf-8" });
}

run("01.in", "01.out");
run("02.in", "02.out");
run("03.in", "03.out");
run("04.in", "04.out");
run("05.in", "05.out");
