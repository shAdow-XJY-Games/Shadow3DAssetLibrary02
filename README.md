# Shadow3DAssetLibrary02

原创 3D 素材库第二卷，承接第一卷封存后的新资产。初始化时本卷资产数为 **0**。

## 仓库分工

- [Shadow3DAssetLibrary](https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary)：第一卷，已闭环的 622 个资产保留原位置，冻结基线为 `3bd5e2f0cb73b1810eaa483a3f42b7721921d094`。不得向此卷追加新资产。
- 本仓库：后续资产源码、交付文件、单资产 manifest 与本卷目录。初始化不复制第一卷资产。
- [Shadow3DAssetGallery](https://github.com/shAdow-XJY-Games/Shadow3DAssetGallery)：独立网页及跨卷目录；网页仓不保存资产本体。仓库链接并不表示网页部署已完成。

## 初始化内容

- `catalog/catalog.json`：本卷目录，`assets` 和 `sources` 均为空。它不是全局网页目录，不能替换第一卷现有 622 项展示。
- `schemas/asset-v1.schema.json`：沿用第一卷的严格资产契约，内容保持一致；其 schema 标识保留兼容来源。
- `schemas/catalog-v1.schema.json`：本卷目录校验契约。
- `config/publishing.json`：明确双仓写入目标、冻结第一卷及分步发布顺序。

## 后续发布约束

全局资产 ID 必须与第一卷和本卷已发布资产排重。先将通过原有 QA 的资产核心文件与单资产 manifest 写入本卷并按真实不可变提交读回；再在网页仓合并跨卷目录图并发布入口。网页发布失败时只续网页阶段，不重复创建已确认的资产提交。各阶段记录独立 journal，绑定仓库、分支、预期 main 与内容 hash，保留历史并拒绝未知结果盲重试。

本初始化不包含新资产、网站部署结果或尚未产生的提交号。
