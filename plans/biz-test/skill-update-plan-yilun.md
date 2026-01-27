# Synnovator Skill 更新计划

## 生成数据id不稳定
执行命令：
```bash
/synnovator create 
```
后，输出的文件有些是 `post_submission_01.md`, 有些是 `post_61dbe7351af8.md`

预期行为：在创建record的时候，所有的id和文件名都一致，格式为`{type}_{uuid}.md`

