SIMPLEAPI = {
    loadData: function (app) {
        app.exts.actions_show = false;
    },
    toolbar: function (type, app) {
        if (type == 'add') {
            treeDialog.add();
            return false
        }

        if (type == 'edit') {

            treeDialog.edit();
            return false
        }
        return true
    },
    init: function (app) {
        var style = document.createElement('style');
        style.type = 'text/css';
        style.innerHTML = `#tree_root .el-checkbox:last-of-type{margin-right:8px;}`;
        document.head.appendChild(style);

        var div = document.createElement('div')
        div.id = 'tree_root';
        div.innerHTML = `<el-dialog width="500px" :title="title" :visible.sync="visible">
    <el-form size="small" ref="treeForm" :model="treeForm" label-width="80px">
      <el-form-item 
        prop="name"
       :rules="[{ required: true, message: '请输入角色名', trigger: 'blur' }]"
      label="角色名">
        <el-input v-model="treeForm.name" placeholder="角色名"></el-input>
      </el-form-item>
      
      <el-form-item label="权限">
            <el-input
              placeholder="输入关键字进行过滤"
              v-model="filterText">
            </el-input>
            <el-tree
              v-loading="loading"
              ref="tree"
              :data="tree"
              @check="checkChange"
              show-checkbox
              :check-strictly="true"
              node-key="id"
              :filter-node-method="filterNode"
              :default-expanded-keys="keys"
              :default-checked-keys="keys"
              :highlight-current="true"
              :default-expand-all="false"
              :auto-expand-parent="true"
              :props="defaultProps">
               <span slot-scope="{ node, data }">
               <i :class="data.icon"></i>
               <span v-text="data.name"></span>
               </span>
            </el-tree>
      </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="visible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm()">确 定</el-button>
      </span>
</el-dialog>`;
        document.body.append(div);

        window.treeDialog = new Vue({
            el: '#tree_root',
            data: {
                title: '添加角色',
                visible: false,
                loading: true,
                filterText: '',
                treeForm: {
                    name: '',
                    id: null
                },
                defaultProps: {
                    children: 'children',
                    label: 'name'
                },
                tree: [],
                keys: [],
            },
            watch: {
                filterText(val) {
                    this.$refs.tree.filter(val);
                }
            },
            created: function () {
                var self = this;
                this.post({
                    action: 'tree'
                }, urls.tree).then(res => {
                    self.tree = res;
                })
            },
            methods: {
                unSelectAll(node) {
                    let self = this;
                    node.checked = false;
                    if(node.childNodes.length!==0){
                        node.childNodes.forEach(n => self.unSelectAll(n));
                    }
                },
                selectAll(node) {
                    let self = this;
                    node.checked = true;
                    if(node.childNodes.length!==0){
                        node.childNodes.forEach(n => self.selectAll(n));
                    }
                },
                checkChange(data) {
                    let node = this.$refs.tree.getNode(data.id);
                    //选中所有的父节点
                    if (node.checked) {
                        let parent = node;
                        while ((parent = parent.parent) != null) {
                            parent.checked = true;
                        }
                        this.selectAll(node);
                    } else {
                        this.unSelectAll(node);
                        //选中或者取消所有的子节点

                    }


                },
                add: function () {

                    //清空表单
                    if (this.$refs.treeForm) {
                        this.$refs.treeForm.resetFields();

                        this.keys = [];
                        this.treeForm.id = null;
                        //清空tree
                        this.$refs.tree.setCheckedKeys([]);
                    }
                    this.$nextTick(function () {
                        this.visible = true;
                    });
                },
                edit: function () {
                    this.loading = true;
                    //为了加速表格显示，关联的权限数据异步查询
                    var self = this;

                    self.visible = true;
                    var row = app.table.selection[0];
                    this.treeForm.id = row._id;
                    this.treeForm.name = row.name;
                    this.keys = [];
                    if (this.$refs.treeForm) {
                        this.$refs.tree.setCheckedKeys([]);
                    }
                    axios.get(urls.role + '?id=' + row._id, {}).then(res => {
                        self.keys = res.data.data;
                    }).finally(__ => {
                        self.loading = false;
                    });
                },
                post: function (params, url) {
                    var self = this;

                    return new Promise((resolve, reject) => {
                        axios.post(url, params).then(res => {
                            var data = res.data;
                            if (Array.isArray(data)) {
                                resolve(data);
                                return;
                            }
                            if (data.state) {
                                resolve(data);
                            } else {
                                reject(data);
                                self.$notify.error({
                                    title: '错误',
                                    message: data.msg
                                });
                            }
                        }).catch(err => {
                            self.$notify.error({
                                title: '错误',
                                message: err
                            });
                        }).finally(__ => {
                            self.loading = false;
                        });
                    });

                },
                filterNode(value, data) {
                    if (!value) return true;
                    return data.label.indexOf(value) !== -1;
                },
                submitForm() {
                    var self = this;
                    this.$refs.treeForm.validate((valid) => {
                        if (valid) {
                            var ids = [];
                            var nodes = self.$refs.tree.getCheckedNodes()
                            for (var i in nodes) {
                                var id = nodes[i].id;
                                if (typeof id != 'undefined') {
                                    ids.push(id);
                                }
                            }
                            var params = {
                                'action': 'save',
                            };
                            if (ids.length != 0) {
                                params['ids'] = ids.join(',');
                            }

                            if (self.treeForm.id) {
                                params['id'] = self.treeForm.id;
                            }

                            params.name = self.treeForm.name;
                            this.post(params, urls.role).then(res => {
                                //关闭对话框
                                self.visible = false;
                                //刷新表格
                                app.refreshData();
                                self.$notify({
                                    title: '成功',
                                    message: '添加成功！',
                                    type: 'success'
                                });
                            });

                        } else {
                            console.log('error submit!!');
                            return false;
                        }
                    });
                },
                //treeDialog.$refs.tree.getCheckedNodes()

            }
        })
    }
}

//自定义html实现
