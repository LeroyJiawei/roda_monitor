<template>
  <div class="quick-container">
    <el-card class="quick-card">
      <v-chart ref="chart2" :options="option2" id="tpc" />
    </el-card>


    <el-dialog title="修改页面" :visible.sync="modifyPageVisible" width="50%" :before-close="handleModifyClose">
      <!-- "id": // 必需
      "name":"", // 必需
      "role": ENUM('supernode', 'source-edge', 'sink-edge', 'hub-edge', 'web-edge') // 必需
      "vlan_addr": "",// 必需
      "servive_port": "" ,  // 可选
      "vlan_name": "",// 必需
      "supernode_name": "",// 必需
      "key":"", // 可选
      "description":"" // 可选
      "addr: "",// 可选 -->
      <el-form :model="modifyNodeData" status-icon ref="modifyNodeData" label-width="130px" class="InputNodeInfo"
        :rules="rulesOfAddNode">

        <el-form-item label="角色" prop="role">
          <el-select filterable class="role_modify_node" v-model="modifyNodeData.role" >
            <!-- v-bind:value绑定的是name值，向上传给了v-model里的modifyNodeData.role -->
            　　　　<el-option v-for="item in edge_enum" :key="item.value" v-bind:value="item.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="名称" prop="name">
          <el-input type="text" v-model="modifyNodeData.name"></el-input>
        </el-form-item>

        <el-form-item label="vlan IP" prop="vlan_addr">
          <el-input type="text" v-model="modifyNodeData.vlan_addr" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="vlan 名称" prop="vlan_name">
          <el-input type="text" v-model="modifyNodeData.vlan_name" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="超节点名称" prop="supernode_name">
          <el-input type="text" v-model="modifyNodeData.supernode_name" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="服务端口">
          <el-input type="text" v-model="modifyNodeData.service_port" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="key">
          <el-input type="text" v-model="modifyNodeData.key" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="描述">
          <el-input type="text" v-model="modifyNodeData.description" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="地址">
          <el-input type="text" v-model="modifyNodeData.addr" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="modifyPageVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitModification('modifyNodeData')">提交修改</el-button>
      </span>
    </el-dialog>



    <el-dialog title="请填入新增节点的信息：" :visible.sync="AddNodeFormVisible" center :append-to-body='0' :lock-scroll="true"
      width="100%">
      <el-form :model="addNodeData" status-icon ref="addNodeData" label-width="130px" class="InputNodeInfo"
        :rules="rulesOfAddNode">
        <!-- prop往上传数据使得rule起作用 -->
        <el-form-item label="name" prop="name">
          <el-input type="text" v-model="addNodeData.name" placeholder='请输入名称(必填)'></el-input>
        </el-form-item>

        <el-form-item label="role" prop="role">
          <el-select filterable class="role_add_node" v-model="addNodeData.role" placeholder='请输入名称(必填)'>
            <!-- v-bind:value绑定的是name值，向上传给了v-model里的addNodeData.role -->
            　　　　<el-option v-for="item in edge_enum" :key="item.value" v-bind:value="item.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="vlan_addr" prop="vlan_addr">
          <el-input type="text" v-model="addNodeData.vlan_addr" placeholder='请输入vlan地址(必填)' auto-complete="off">
          </el-input>
        </el-form-item>

        <el-form-item label="vlan_name" prop="vlan_name">
          <el-input type="text" v-model="addNodeData.vlan_name" placeholder='请输入vlan名称(必填)' auto-complete="off">
          </el-input>
        </el-form-item>

        <el-form-item label="supernode_name" prop="supernode_name">
          <el-input type="text" v-model="addNodeData.supernode_name" placeholder='请输入超节点名称(必填)' auto-complete="off">
          </el-input>
        </el-form-item>

        <el-form-item label="service_port">
          <el-input type="text" v-model="addNodeData.service_port" placeholder='(可选)' auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="key">
          <el-input type="text" v-model="addNodeData.key" placeholder='(可选)' auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="description">
          <el-input type="text" v-model="addNodeData.description" placeholder='(可选)' auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="addr">
          <el-input type="text" v-model="addNodeData.addr" placeholder='(可选)' auto-complete="off"></el-input>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="AddNodeFormVisible = false; resetForm('addNodeData')">取 消</el-button>
        <el-button type="primary" @click="submitNodeInfo('addNodeData')"> 增加节点 </el-button>
      </div>

    </el-dialog>


    <el-card style="margin-top:20px">

      <div v-show="true" class="select">
        <span v-text='tableHeadText' style="font-size:18px">
        </span>
        　　<el-select filterable class="choice" v-on:change="indexSelect" v-model="edge_enum_choose">
          <!-- v-bind:value绑定的是name值，向上传给了v-model里的edge_enum_choose -->
          　　　　<el-option v-for="item in edge_enum" :key="item.value" v-bind:value="item.name"></el-option>
          　　</el-select>

        <span>
          <el-button type="primary" v-on:click="AddNodeFormVisible = true" style="margin:10px 0;">新增节点</el-button>
        </span>
      </div>


      <!-- stripe 是带斑马纹（相邻两行不同背景） -->
      <el-table :data="tableData" stripe :border="true" style="width: 100%" max-height="2500">
        <el-table-column prop="role" label="角色">
        </el-table-column>

        <el-table-column prop="name" label="名称">
        </el-table-column>

        <el-table-column prop="vlan_addr" label="vlan IP">
        </el-table-column>


        <el-table-column prop="vlan_name" label="vlan 名称">
        </el-table-column>

        <el-table-column prop="service_port" label="服务端口">
        </el-table-column>

        <el-table-column prop="supernode_name" label="超节点名称">
        </el-table-column>

        <el-table-column prop="create_time" label="创建时间" sortable>
        </el-table-column>

        <el-table-column prop="update_time" label="更新时间" sortable>
        </el-table-column>

        <el-table-column prop="state" label="状态">
        </el-table-column>

        <el-table-column prop="addr" label="地址">
        </el-table-column>

        <el-table-column label="操作" fixed="right">
          <template slot-scope="scope">
            <span>
              <el-button style="display:block;margin:0 auto;height:35px;"
                @click.native.prevent="modifyARow(scope.$index)" type="text" size="small">
                修改
              </el-button>
            </span><span>
              <el-button style="display:block;margin:0 auto;height:35px;"
                @click.native.prevent="deleteRow(scope.$index)" type="danger" size="small">
                删除
              </el-button>
            </span>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>

</template>

<script>
  import ECharts from "vue-echarts";
  // import "echarts/lib/chart/line";
  // import "echarts/lib/component/polar";
  import echarts from "echarts";

  // import obj from "../common/enum_edge";
  // import Enum from "../common/Enum";

  var data2 = [
    {
      symbolSize: 20,
      id: 0,
      name: "super",
    },
    {
      id: 1,
      symbolSize: 20,
      name: "edge1",
    },
    {
      id: 2,
      symbolSize: 20,
      name: "edge2",
    },
    {
      id: 3,
      symbolSize: 20,
      name: "edge3",
    },
  ];

  var edges2 = [
    {
      source: 0,
      target: 1,
      lineStyle: {
        width: 5,
        curveness: 0.2,
      },
    },
    {
      source: 0,
      target: 2,
      lineStyle: {
        width: 5,
        curveness: 0.2,
      },
    },
    {
      source: 0,
      target: 3,
      lineStyle: {
        width: 5,
        curveness: 0.2,
      },
    },
  ];

  // let sourceTypeList =this.$enum.getValueDescList('SOURCE_IN_TYPE')  

  export default {
    components: {
      "v-chart": ECharts,
    },

    data() {
      return {
        rulesOfAddNode: {
          name: [
            { required: true, trigger: 'blur' },
            { min: 1, message: '不能为空', trigger: 'blur' }
          ],
          role: [
            { required: true, trigger: 'blur' },
            { min: 1, message: '不能为空', trigger: 'blur' }
          ],
          vlan_addr: [
            { required: true, trigger: 'blur' },
            { min: 1, message: '不能为空', trigger: 'blur' }
          ],
          vlan_name: [
            { required: true, trigger: 'blur' },
            { min: 1, message: '不能为空', trigger: 'blur' }
          ],
          supernode_name: [
            { required: true, trigger: 'blur' },
            { min: 1, message: '不能为空', trigger: 'blur' }
          ],
        },
        AddNodeFormVisible: false, // 是否显示新增节点框
        modifyPageVisible: false,
        addNodeData: {
          name: "",
          role: "",
          vlan_addr: "",
          vlan_name: "",
          supernode_name: "",
          service_port: "", // 以下可选
          key: "",
          description: "",
          addr: ""
        },
        modifyNodeData: {
          id: "",
          name: "",
          role: "",
          vlan_addr: "",
          vlan_name: "",
          supernode_name: "",
          service_port: "", // 以下可选
          key: "",
          description: "",
          addr: ""
        },
        tableHeadText: '请选择表格类型：',
        edge_enum_choose: 'supernode',   //  表格类型选择值记录
        edge_enum: [{
          "indexId": 1,
          "name": "supernode"
        }, {
          "indexId": 2,
          "name": "source-edge"
        }, {
          "indexId": 3,
          "name": "sink-edge"
        }, {
          "indexId": 4,
          "name": "hub-edge"
        }, {
          "indexId": 5,
          "name": "web-edge"
        }, {
          "indexId": 6,
          "name": "all"
        }],

        tableData: [{
          id: "009",
          role: 'sink',
          name: '王小虎',
          vlan_addr: '1.1.1.1',
          vlan_name: 'v1',
          service_port: 50,
          supernode_name: 'n1',
          create_time: '2020-9-14',
          update_time: '2020-9-15',
          state: 'open',
          addr: '129号'
        }],
        option2: {
          grid: {
            top: '14%',
            bottom: '18%',
            left: '15%',
            right: '4%',
          },
          series: [
            {
              type: "graph",
              layout: "force",
              animation: true,
              data: data2,
              force: {
                // repulsion: 200,
                edgeLength: 300,
              },
              edgeSymbolSize: 1200,
              edges: edges2,
            },
          ],
        },
      };
    },
    created() {
      this.edge_enum_choose = this.edge_enum[0].name;
    },

    methods: {
      handleModifyClose(done) {
        this.$confirm('确认放弃修改？')
          .then(_ => {
            done();
          })
          .catch(_ => { });
      },
      modifyARow(index) { // 弹出出修改对话框
       
        // 从表格中获取部分数据(相交的）而不是全部!所以单独列出
        this.modifyNodeData.id=this.tableData[index].id;
        this.modifyNodeData.role=this.tableData[index].role;
        this.modifyNodeData.name=this.tableData[index].name;
        this.modifyNodeData.vlan_addr=this.tableData[index].vlan_addr;
        this.modifyNodeData.vlan_name=this.tableData[index].vlan_name;
        this.modifyNodeData.supernode_name=this.tableData[index].supernode_name;
        this.modifyNodeData.service_port=this.tableData[index].service_port;
        this.modifyNodeData.addr=this.tableData[index].addr;

        this.modifyPageVisible = true;
      },
      submitModification(formName) {
        this.modifyPageVisible = false;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios
              ({
                url: `${window.$config.HOST}/api/n2n/update`,
                method: 'post',
                data: this.modifyNodeData, // body参数
              })
              .then((response) => {
                console.log(response);
                if (response.data.status == "OK") {
                  alert('修改成功！');
                  // 清空新增数据信息
                  this.modifyNodeData = {
                    id: "",
                    name: "",
                    role: "",
                    vlan_addr: "",
                    vlan_name: "",
                    supernode_name: "",
                    service_port: "", // 以下可选
                    key: "",
                    description: "",
                    addr: ""
                  };
                }
                else {
                  alert(response.data.status);
                  alert('修改失败!');
                }
              })
              .catch((error) => {
                console.log(error);
                alert('修改失败');
              });
          } else {
            // console.log('error submit!!');
            return false;
          }
        });
      },
      deleteRow(index) {
        // console.log(this.tableData[index].id);
        this.$axios
          ({
            url: `${window.$config.HOST}/api/n2n/delete`,
            method: 'delete',
            data: { "id": this.tableData[index].id }, // body参数
          })
          // 下面这种方式显示500错误
          // .delete(`${window.$config.HOST}/api/n2n/delete`, 
          //   {"id":this.tableData[index].id}
          // )
          .then((response) => {
            // console.log(response);
            if (response.data.status == "OK") {
              alert('删除成功！');
            }
            else {
              alert(response.data.status)
              alert('删除失败!');
            }
          })
          .catch((error) => {
            console.log(error);
            alert('删除失败');
          });
      },
      resetForm(formName) {  //  重置，取消新增节点后清空输入的节点信息
        this.$refs[formName].resetFields();
      },
      submitNodeInfo: function (formName) {  //  新增节点
        // console.log(this.addNodeData)
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.AddNodeFormVisible = false;
            // console.log(this.addNodeData);
            this.$axios
              ({
                url: `${window.$config.HOST}/api/n2n/register`,
                method: 'post',
                data: this.addNodeData
                // data: {
                //   name: this.addNodeData.name,
                //   role: this.addNodeData.role,
                //   vlan_addr: this.addNodeData.vlan_addr,
                //   vlan_name: this.addNodeData.vlan_name,
                //   supernode_name: this.addNodeData.supernode_name,
                //   service_port: this.addNodeData.service_port, // 以下可选
                //   key: this.addNodeData.key,
                //   description: this.addNodeData.description,
                //   addr: this.addNodeData.addr
                // } // body参数
              })
              // .post(`${window.$config.HOST}/api/n2n/register`,
              //   {data:this.addNodeData}
              // )
              .then((response) => {
                console.log(response);
                // 清空新增数据信息
                this.addNodeData = {
                  name: "",
                  role: "",
                  vlan_addr: "",
                  vlan_name: "",
                  supernode_name: "",
                  service_port: "", // 以下可选
                  key: "",
                  description: "",
                  addr: ""
                };
                if (response.data.status == "OK") {
                  alert('增加成功！');
                }
              })
              .catch((error) => {
                console.log(error);
                alert('增加失败');
              });

          } else {
            // console.log('error submit!!');
            return false;
          }
        });

      },

      // 修改表格类型后重新获取数据
      indexSelect() {
        // console.log(this.edge_enum_choose);
        // this.getTableData();
        this.getTopoData()
      },

      async getTopoData() {
        const _this = this
        await this.$axios
          .get(`${window.$config.HOST}/api/n2n/topo`)
          // .get(`https://easy-mock.com/mock/5f6736c27304034f4b7541d4/api/n2n/topo`)
          .then((response) => {
            // alert('begin to get Topo');
            // console.log(response.data)
            _this.data2 = response.data.data.nodes;
            _this.edges2 = response.data.data.edges;

            var optionOfTopo = {
              title: {
                show: true,
                text: '系统拓扑图',
                subtext: 'source和sink节点',
                left: "auto",
                top: "auto",
              },
              grid: {
                top: '14%',
                bottom: '18%',
                left: '15%',
                right: '4%',
              },
              legend: [{
                selectedMode: 'single',
                // data: categories.map(function (a) {
                //   return a.name;
                // })
              }],
              animationDuration: 3000,
              coordinateSystem: 'none',
              hoverAnimation: 1,
              // legend: [{
              //   data: ["类目0", "类目1", "类目2", "类目3", "类目4", "类目5", "类目6", "类目7", "类目8"]
              // }],
              // animationEasingUpdate: 'quinticInOut',
              // categories: [{
              //   name: "类目0"
              // }, {
              //   name: "类目1"
              // }, {
              //   name: "类目2"
              // }, {
              //   name: "类目3"
              // }, {
              //   name: "类目4"
              // }, {
              //   name: "类目5"
              // }, {
              //   name: "类目6"
              // }, {
              //   name: "类目7"
              // }, {
              //   name: "类目8"
              // }],
              series: [
                {
                  zoom: 0.6,  // 缩放比例
                  type: "graph",
                  layout: "circular",    // "force"
                  name: "source or sink",

                  circular: {
                    rotateLabel: true
                  },
                  symbolSize: 30,  //  节点大小
                  // edgeSymbol: ['circle', 'arrow'],
                  animation: true,
                  data: _this.data2,
                  edges: _this.edges2,

                  edgeSymbolSize: 120,


                  focusNodeAdjacency: 1,
                  itemStyle: {// 点周围的阴影
                    borderColor: '#ffff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.6)'
                  },
                  roam: true,
                  label: {
                    position: 'right',
                    formatter: '{b}',
                    fontStyle: "oblique",
                    fontWeight: "bolder",
                    fontFamily: "Segoe Print",
                    color: "rgba(50, 15, 15, 1)",
                    fontSize: 20 // 标签的字体大小
                  },
                  lineStyle: {
                    color: "rgba(205, 130, 130, 30)",
                    curveness: 0.4,
                    width: 4,
                    type: "solid",
                    shadowBlur: 1
                  },
                  emphasis: {
                    lineStyle: {
                      width: 10
                    }
                  }
                },
              ],
            };
            // _this.data2.symbolSize=50;
            var theTopoChart = echarts.init(document.getElementById('tpc'));
            theTopoChart.setOption(optionOfTopo, true);
            // console.log(_this.edges2);
            // console.log(_this.data2);
            // alert('goodTopo');
          })
          .catch((error) => {
            console.log(error);
            alert('bad-topo-data');
          });

        await this.$axios
          .get(`${window.$config.HOST}/api/n2n/list`, {
            params: {
              "role": this.edge_enum_choose // 必需
            }
          })
          .then((response) => {
            _this.tableData = response.data.data;
            // console.log(_this.tableData);
            // alert('goodTableData')
          })
          .catch((error) => {
            console.log(error);
            alert('bad-table-data');
          });

      },

      async getTableData() {   // 这个函数不能和getTopoData同时执行，所以放到了getTopoData里面
        const _this = this
        alert('begin to get table data')
        await this.$axios
          .get(`${window.$config.HOST}/api/n2n/list`, {
            params: {
              "role": this.edge_enum[this.edge_enum_choose - 1].name // 必需
            }
          })
          .then((response) => {
            _this.tableData = response.data.data;
            console.log(_this.tableData);
            alert('goodTableData')
          })
          .catch((error) => {
            console.log(error);
            alert('bad-table-data');
          });
      }
    },

    mounted() {
      this.getTopoData();
      // this.getTableData()
    }
  };
</script>

<style lang="less" scoped>
  .quick-container {
    .quick-card {
      height: 80vh;

      .echarts {
        width: 100%;
        height: 750px;
      }

      .el-card__header {
        padding: 0 20px;
        height: 48px;
        line-height: 48px;
      }

      .el-card__body {
        height: 100%;
      }

      .el-step__description {
        margin-top: 15px;

        p {
          line-height: 1.5;
        }
      }
    }
  }
</style>