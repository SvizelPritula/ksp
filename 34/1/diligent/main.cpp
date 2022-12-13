#include <algorithm>
#include <iostream>
#include <set>
#include <vector>

struct task {
  long value;
  long deadline;
  int id;
};

struct segment {
  long start;
  long end;
};

bool operator<(task a, task b) { return a.value > b.value; }

bool operator<(segment a, segment b) { return a.start < b.start; }

std::vector<long> solve(std::vector<task> tasks) {
  std::vector<long> results(tasks.size());
  std::fill(results.begin(), results.end(), -1);

  std::sort(tasks.begin(), tasks.end());

  std::set<segment> shedule;

  for (task t : tasks) {
    int time = t.deadline;

    auto container = shedule.upper_bound({t.deadline, 0});
    if (container != shedule.begin()) {
      container--;
      if (container->end >= t.deadline) {
        time = container->start - 1;
      }
    }

    if (time < 0) continue;
    results[t.id] = time;

    segment seg = {time, time};

    auto next = shedule.upper_bound({time, 0});

    if (next != shedule.end()) {
      if (next->start == time + 1) {
        seg.end = next->end;
        shedule.erase(*next);
      }
    }

    auto prev = shedule.upper_bound({time, 0});
    if (prev != shedule.begin()) {
      prev--;

      if (prev->end == time - 1) {
        seg.start = prev->start;
        shedule.erase(*prev);
      }
    }

    shedule.insert(seg);
  }

  return results;
}

int main() {
  std::iostream::sync_with_stdio(false);

  int taskCount;
  std::vector<task> tasks;

  std::cin >> taskCount;

  tasks.reserve(taskCount);

  for (int i = 0; i < taskCount; i++) {
    int value, deadline;
    std::cin >> value >> deadline;

    tasks.push_back({
        value,
        deadline,
        i
    });
  }

  std::vector<long> times = solve(tasks);
  long points = 0;

  for (int i = 0; i < times.size(); i++) {
    if (times[i] >= 0) {
      points += tasks[i].value;
    }
  }

  std::cout << points << std::endl;

  for (long t : times) {
    std::cout << t << std::endl;
  }

  return 0;
}