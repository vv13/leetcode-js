import os
import json

LEETCODE_URL = 'https://leetcode.com/problems/'


def genLineStr(s: str):
    number, name, difficulty = s.split('.')
    source_dir = './leetcode/%s/' % s
    link_name = '[{0}]({1})'.format(name, source_dir)
    link_leetcode = '[原题]({0})'.format(LEETCODE_URL + name)
    link_answer = '[答案]({0})'.format(source_dir + '/solution.py') # TODO: find newest answer
    tags = []
    mark = ''
    if os.path.exists(source_dir + 'relation.json'):
        relation_file = open(source_dir + '/relation.json', 'r')
        relation_data = json.load(relation_file)
        tags = relation_data.get('tags', [])
        mark = relation_data.get('mark', '')
        relation_file.close()

    return '|{0}|{1}|{2}|{3}|{4}|{5}|'.format(number, link_name, difficulty, ', '.join(tags), '  '.join([link_answer, link_leetcode]), mark)


file = open('README.md', 'w')
file.write('''
## leetcode
| 序号 | 名称 | 难度 | 标签 | 链接 | 备注 |
| :----:| :---- | :----: | :----: | :----: | :---- |
''')
leetcodes = [genLineStr(i) for i in sorted(os.listdir('./leetcode')) if i != 'utility']
file.write(os.linesep.join(leetcodes))
file.write('''
## 开启你的刷题之旅
### 获取题目信息
选取你想要练习的题目编号，通过 [leetcode-problems-crawler](https://github.com/vv13/leetcode-problems-crawler) 进行题目信息爬取：
```
npx leetcode-problems-crawler  -l python3 -r 1
```

此时会在当前文件夹下生成如下目录：
```
001.two-sum.easy
├── README.md
└── solution.py
```

### 编写测试代码
我实现了一个比较简单的代码执行器，首先将文件 `leetcode/utility/test_runner.py` 复制到文件夹中，并创建 `test.py` 文件，此时的目录信息为：
```
001.two-sum.easy
├── README.md
└── solution.py
├── test_runner.py
├── test.py
```

打开 `test.py`，编写通用测试代码，并添加一个测试用例数据：
```

from test_runner import testRunner
from solution import Solution


if __name__ == "__main__":
    inputs = [
        [[2, 7, 11, 15], 9]
    ]
    expects = [[0, 1]] # 可不传此结果集，直接观察输出结果
    testRunner(inputs, Solution, expects)
```

没错，执行测试代码就是这么简单，`testRunner` 会自动解析所有类方法，并将 `inputs` 数组通过正确的形式进行传入，现在编写 `solution.py`，让我们来实现两种不同的解法：
```python
from typing import List

class Solution(object):
    # brute force
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if (nums[i] + nums[j]) == target:
                    return [i, j]

    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        map = {}
        for index, cur in enumerate(nums):
            expect = target - cur
            if expect in map:
                return [map[expect], index]
            map[cur] = index

```

之后，直接执行 `test.py` 观察输出结果：
```
$ python test.py
twoSum :
result: [0, 1], passed
all test passed

twoSum1 :
result: [0, 1], passed
all test passed

```

若需要生成 README，请参考 `generate_markdown.py` 文件，欢迎 star 或 folk。
''')
file.close()
