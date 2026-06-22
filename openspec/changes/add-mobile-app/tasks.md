## 1. 项目初始化

- [ ] 1.1 创建 Flutter 项目（flutter create family_agent_app）
- [ ] 1.2 配置 pubspec.yaml 依赖（http、image_picker、file_picker、record、audioplayers）
- [ ] 1.3 创建目录结构（screens/widgets/services/models）

## 2. 基础 UI 结构

- [ ] 2.1 创建 HomeScreen 主页面
- [ ] 2.2 创建 InputModeSelector 输入模式选择器
- [ ] 2.3 实现底部导航或 Tab 切换

## 3. 文本输入组件

- [ ] 3.1 创建 TextInputWidget
- [ ] 3.2 实现文本输入和发送逻辑
- [ ] 3.3 添加加载状态和错误处理

## 4. 文件上传组件

- [ ] 4.1 创建 FileUploadWidget
- [ ] 4.2 使用 file_picker 实现文件选择
- [ ] 4.3 支持 JSON/CSV/TXT 文件
- [ ] 4.4 添加文件预览

## 5. 图片上传组件

- [ ] 5.1 创建 ImageUploadWidget
- [ ] 5.2 使用 image_picker 实现相册选择和相机拍摄
- [ ] 5.3 添加图片预览
- [ ] 5.4 压缩大图片（如需要）

## 6. 语音录制组件

- [ ] 6.1 创建 VoiceRecordWidget
- [ ] 6.2 使用 record 实现录音功能
- [ ] 6.3 实现录音/停止/播放
- [ ] 6.4 处理麦克风权限
- [ ] 6.5 添加录音超时处理

## 7. API 服务集成

- [ ] 7.1 创建 ApiService 服务类
- [ ] 7.2 实现 /api/add 文本输入
- [ ] 7.3 实现 /api/add 文件上传
- [ ] 7.4 实现 /api/add 图片上传
- [ ] 7.5 实现 /api/add 语音上传
- [ ] 7.6 实现 /api/search 搜索
- [ ] 7.7 实现 /api/members 列表
- [ ] 7.8 实现 /api/profile/:name 详情
- [ ] 7.9 添加网络错误处理和重试

## 8. 结果展示组件

- [ ] 8.1 创建 ResponseDisplay widget
- [ ] 8.2 格式化显示添加/搜索结果
- [ ] 8.3 添加成功/失败状态展示

## 9. 测试和发布

- [ ] 9.1 iOS 模拟器测试
- [ ] 9.2 Android 模拟器/真机测试
- [ ] 9.3 iOS App Store 发布配置
- [ ] 9.4 Google Play Store 发布配置
- [ ] 9.5 端到端测试：移动 App → REST API → 数据存储
