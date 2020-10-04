<template>
  <div class="sink-source-container">
    <el-card>
      <v-chart ref="chart2" :options="option2" id="tpc" />
    </el-card>

    <el-dialog title="修改页面" :visible.sync="ModifyPageVisible" width="50%" :before-close="handleModifyClose"
      :modal-append-to-body="false">
      <el-form :model="modifyNodeData" status-icon ref="modifyNodeData" label-width="130px" class="ModifyNodeInfo"
        :rules="rulesOfNode">
        <el-form-item label="名称" prop="name">
          <el-input type="text" v-model="modifyNodeData.name"></el-input>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select filterable class="role_modify_node" v-model="modifyNodeData.role" placeholder="请选择角色(必选)">
            　　　　<el-option v-for="item in role_add_modify" :key="item.value" v-bind:value="item.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="网络名称" prop="network_id">
          <el-select filterable clearable class="netid_modify_node" v-model="modifyNodeData.network_id" placeholder="请选择网络">
            　　　　<el-option v-for="item in network_id_option"  :label="item.name" :key="item.id" v-bind:value="item.id.toString()">
              <span style="float: left">{{ item.name }}</span> <!-- :label指定是选中后框框里显示的内容，v-bind:value是实际绑定的内容！-->
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.id }}</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据源系统" prop="source_data_system">
          <el-select filterable class="dss_add_node" v-model="modifyNodeData.source_data_system"
            placeholder="请选择数据源系统(必选)">
            　　　　<el-option v-for="item in data_source_system" :key="item.value" v-bind:value="item.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据源信息" prop="source_info">
          <el-input type="text" v-model="modifyNodeData.source_info" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="ap主机名" prop="ap_hostname">
          <el-input type="text" v-model="modifyNodeData.ap_hostname" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input type="text" v-model="modifyNodeData.description" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="docker端口号" prop="docker_port">
          <el-input type="text" v-model="modifyNodeData.docker_port" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="
            ModifyPageVisible = false;
            resetNodeForm('modifyNodeData');
          ">取 消</el-button>
        <el-button type="primary" @click="submitModification('modifyNodeData')">提交修改</el-button>
      </span>
    </el-dialog>

    <el-dialog title="请填入新增节点的信息：" :visible.sync="AddNodePageVisible" center :append-to-body="0" :lock-scroll="true"
      width="100%" :modal-append-to-body="false" :before-close="handleAddClose">
      <el-form :model="addNodeData" status-icon ref="addNodeData" label-width="130px" class="AddNodeInfo"
        :rules="rulesOfNode">
        <!-- prop往上传数据使得rule起作用 -->
        <el-form-item label="名称" prop="name">
          <el-input type="text" v-model="addNodeData.name" placeholder="请输入名称(必填)"></el-input>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select filterable class="role_add_node" v-model="addNodeData.role" placeholder="请选择角色(必选)">
            <!-- v-bind:value绑定的是name值，向上传给了v-model里的addNodeData.role -->
            　　　　<el-option v-for="item in role_add_modify" :key="item.value" v-bind:value="item.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="网络名称" prop="network_id">
          <el-select filterable clearable class="netid_add_node" v-model="addNodeData.network_id" placeholder="请选择网络">
            　　　　<el-option v-for="item in network_id_option"  :label="item.name" :key="item.id" v-bind:value="item.id.toString()">
              <span style="float: left">{{ item.name }}</span> <!-- :label指定是选中后框框里显示的内容，v-bind:value是实际绑定的内容！-->
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.id }}</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据源系统" prop="source_data_system">
          <el-select filterable class="dss_add_node" v-model="addNodeData.source_data_system"
            placeholder="请选择数据源系统(必选)">
            <!-- v-bind:value绑定的是name值，向上传给了v-model里的addNodeData.role -->
            　　　　<el-option v-for="item in data_source_system" :key="item.value" v-bind:value="item.name"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据源信息" prop="source_info">
          <el-input type="text" v-model="addNodeData.source_info" placeholder="请输入数据源信息(必填)" auto-complete="off">
          </el-input>
        </el-form-item>

        <el-form-item label="ap主机名" prop="ap_hostname">
          <el-input type="text" v-model="addNodeData.ap_hostname" placeholder='请输入ap主机名(role为"source"时必填)'
            auto-complete="off">
          </el-input>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input type="text" v-model="addNodeData.description" placeholder="请输入描述(可选)" auto-complete="off">
          </el-input>
        </el-form-item>

        <el-form-item label="docker端口" prop="docker_port">
          <el-input type="text" v-model="addNodeData.docker_port" placeholder="请输入docker端口(可选)" auto-complete="off">
          </el-input>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="
            AddNodePageVisible = false;
            resetNodeForm('addNodeData');
          ">取 消</el-button>
        <el-button type="primary" @click="submitAddNode('addNodeData')">
          增加节点
        </el-button>
      </div>
    </el-dialog>

    <el-card style="margin-top: 20px">
      <div v-show="true" class="select">
        <span v-text="tableHeadText" style="font-size: 18px"></span>
        　　<el-select filterable class="choice" v-on:change="indexSelect" v-model="edge_enum_choose">
          　　　　<el-option v-for="item in edge_enum" :key="item.value" v-bind:value="item.name"></el-option>
          　　</el-select>
        <span>
          <el-button type="primary" v-on:click="openAddNodeDialog()" style="margin: 10px 0">新增节点</el-button>
        </span>
      </div>

      <el-table :data="tableData" stripe :border="true" style="width: 100%" max-height="2500">
        <el-table-column prop="name" label="名称"> </el-table-column>

        <el-table-column prop="role" label="角色"> </el-table-column>

        <el-table-column prop="network_name" label="网络名称">
        </el-table-column>

        <el-table-column prop="create_time" label="创建时间"> </el-table-column>

        <el-table-column prop="update_time" label="更新时间"> </el-table-column>

        <el-table-column prop="state" label="状态"> </el-table-column>

        <el-table-column prop="source_data_system" label="数据源系统">
        </el-table-column>

        <el-table-column prop="source_info" label="数据源信息">
        </el-table-column>

        <el-table-column prop="description" label="描述"> </el-table-column>

        <el-table-column prop="docker_port" label="docker端口">
        </el-table-column>

        <el-table-column prop="ap_hostname" label="ap主机名"> </el-table-column>

        <el-table-column label="操作" fixed="right">
          <template slot-scope="scope">
            <span>
              <el-button style="display: block; margin: 0 auto; height: 35px"
                @click.native.prevent="modifyARow(scope.$index)" type="text" size="small">
                修改
              </el-button>
            </span><span>
              <el-button style="display: block; margin: 0 auto; height: 35px"
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

  export default {
    components: {
      "v-chart": ECharts,
    },

    data() {
      return {
        AddNodePageVisible: false, // 是否显示新增节点框
        ModifyPageVisible: false,
        addNodeData: {
          name: "",
          role: "",
          network_id: "",
          source_info: "",
          source_data_system: "",
          ap_hostname: "", //可选，role为"source"时必需
          description: "", // 可选
          docker_port: "", // 可选
        },
        modifyNodeData: {
          id: "",
          name: "",
          role: "",
          network_id: "",
          source_info: "",
          source_data_system: "",
          ap_hostname: "", //可选，role为"source"时必需
          description: "", // 可选
          docker_port: "", // 可选
        },
        rulesOfNode: {
          id: [
            { required: true, trigger: "blur" },
            { min: 1, message: "不能为空", trigger: "blur" },
          ],
          name: [
            { required: true, trigger: "blur" },
            { min: 1, message: "不能为空", trigger: "blur" },
          ],
          role: [
            { required: true, trigger: "blur" },
            { min: 1, message: "不能为空", trigger: "blur" },
          ],
          network_id: [
            { required: true, trigger: "blur" },
            { min: 1, message: "不能为空", trigger: "blur" },
          ],
          source_info: [
            { required: true, trigger: "blur" },
            { min: 1, message: "不能为空", trigger: "blur" },
          ],
          source_data_system: [
            { required: true, trigger: "blur" },
            { min: 1, message: "不能为空", trigger: "blur" },
          ],
        },
        tableHeadText: "请选择表格类型：",
        edge_enum_choose: "sink",
        edge_enum: [
          {
            indexId: 1,
            name: "all",
          },
          {
            indexId: 2,
            name: "sink",
          },
          {
            indexId: 3,
            name: "source",
          },
        ],
        role_add_modify: [
          // 新增或修改时role的下拉框
          {
            indexId: 1,
            name: "sink",
          },
          {
            indexId: 2,
            name: "source",
          },
        ],
        data_source_system: [
          {
            indexId: 1,
            name: "kafka",
          },
          {
            indexId: 2,
            name: "mysql",
          },
          {
            indexId: 3,
            name: "redis",
          },
        ],
        network_id_option: {}, // 用于修改框中network_id的选择，将其中的name作为network_id的下拉框数据，将对应name的id作为network_id
        tableData: [
          {
            id: "",
            role: "sink",
            name: "王小虎",
            network_id: "1.1.1.1",
            network_name: "n1",
            create_time: "2020-9-14",
            update_time: "2020-9-15",
            state: "open",
            source_data_system: "kafka",
            source_info: "source info",
            description: "",
            docker_port: "",
            ap_hostname: "1.1.1.2",
          },
        ],
        option2: {
          grid: {
            top: "14%",
            bottom: "10%",
            left: "15%",
            right: "4%",
          },
          series: [
            {
              type: "graph",
              layout: "force",
              animation: false,
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
      deleteRow(index) {
        // console.log(this.tableData[index].id);
        this.$axios({
          url: `${window.$config.HOST}/api/sink_source/delete`,
          method: "delete",
          data: { id: this.tableData[index].id }, // body参数
        })
          // 下面这种方式显示500错误
          // .delete(`${window.$config.HOST}/api/n2n/delete`,
          //   {"id":this.tableData[index].id}
          // )
          .then((response) => {
            if (response.data.status == "OK") {
              alert("删除成功！");
              this.getTopoAndTableData(); // 刷新数据
            } else {
              alert(response.data.status);
              alert("删除失败!");
            }
          })
          .catch((error) => {
            console.log(error);
            alert("删除失败");
          });
      },

      handleModifyClose(done) {
        // this.$confirm("确认放弃修改？")
        //   .then((_) => {
        //     // 清空新增数据信息
        //     this.modifyNodeData = {
        //       id: "",
        //       name: "",
        //       role:"",
        //       network_id: "",
        //       source_info: "",
        //       source_data_system: "",
        //       ap_hostname: "",
        //       description: "", // 可选
        //       docker_port: "", // 可选
        //     };
        //     done();
        //   })
        //   .catch((_) => { });
        this.modifyNodeData = {
          id: "",
          name: "",
          role: "",
          network_id: "",
          source_info: "",
          source_data_system: "",
          ap_hostname: "",
          description: "", // 可选
          docker_port: "", // 可选
        };
        this.ModifyPageVisible = false;
      },
      modifyARow(index) {
        // 弹出修改对话框
        // 从表格中获取部分数据(相交的）而不是全部!所以单独列出
        this.modifyNodeData.id = this.tableData[index].id.toString();
        this.modifyNodeData.name = this.tableData[index].name;
        this.modifyNodeData.role = this.tableData[index].role;
        // this.modifyNodeData.network_id = this.tableData[index].network_id.toString();
        this.modifyNodeData.network_id = this.tableData[index].network_name;
        this.modifyNodeData.source_info = this.tableData[index].source_info;
        this.modifyNodeData.source_data_system = this.tableData[
          index
        ].source_data_system;
        this.modifyNodeData.description = this.tableData[index].description;
        this.modifyNodeData.docker_port = this.tableData[index].docker_port;
        this.modifyNodeData.ap_hostname = this.tableData[index].ap_hostname;
        this.ModifyPageVisible = true;

        this.$axios
          .get(`${window.$config.HOST}/api/network/list`, {
            params: {
              role: "all",
            },
          })
          .then((response) => {
            // this.network_id_option = response.data.data;
            // this.network_id_option = new Map();  //构造map方法
            // for (let i of response.data.data) {
            //   this.network_id_option.set(i.id,i.name);
            // }
            this.network_id_option = response.data.data;
            // console.log(this.network_id_option);
          })
          .catch((error) => {
            console.log(error);
            alert("网络页面的表格数据获取失败，通信错误！");
          });
      },
      submitModification(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            // console.log(this.modifyNodeData.network_id);
            this.$axios({
              url: `${window.$config.HOST}/api/sink_source/update`,
              method: "post",
              data: this.modifyNodeData, // body参数
            })
              .then((response) => {
                console.log(response);
                if (response.data.status == "OK") {
                  alert("修改成功！");
                  this.getTopoAndTableData(); // 刷新数据
                  this.ModifyPageVisible = false;
                  // 清空新增数据信息
                  this.modifyNodeData = {
                    id: "",
                    name: "",
                    network_id: "",
                    source_info: "",
                    source_data_system: "",
                    ap_hostname: "",
                    description: "", // 可选
                    docker_port: "", // 可选
                  };
                  this.getTopoAndTableData(); // 刷新表格
                } else {
                  alert("修改失败!");
                  console.log(response);
                }
              })
              .catch((error) => {
                console.log(error);
                alert("修改失败，前后端通信错误");
              });
          } else {
            alert("请填满相关内容");
            return false;
          }
        });
      },

      // 新增节点相关函数：
      resetNodeForm(formName) {
        //  重置，点击取消按钮后清空输入的节点信息
        this.$refs[formName].resetFields();
      },
      handleAddClose(done) {
        // this.$confirm("确认放弃新增节点？")
        //   .then((_) => {
        //     // 清空新增数据信息
        //     this.addNodeData = {
        //       name: "",
        //       role: "",
        //       network_id: "",
        //       source_info: "",
        //       source_data_system: "",
        //       ap_hostname: "",
        //       description: "", // 可选
        //       docker_port: "", // 可选
        //     };
        //     done();
        //   })
        //   .catch((_) => { });
        this.addNodeData = {
          name: "",
          role: "",
          network_id: "",
          source_info: "",
          source_data_system: "",
          ap_hostname: "",
          description: "", // 可选
          docker_port: "", // 可选
        };
        this.AddNodePageVisible = false;
      },
      openAddNodeDialog() {
        this.$axios
          .get(`${window.$config.HOST}/api/network/list`, {
            params: {
              role: "all",
            },
          })
          .then((response) => {
            this.network_id_option = response.data.data;
            // console.log(this.network_id_option);
          })
          .catch((error) => {
            console.log(error);
            alert("网络页面的表格数据获取失败，通信错误！");
          });
        this.AddNodePageVisible = true;
      },
      async submitAddNode(formName) {
        //  新增节点
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if (
              this.addNodeData.ap_hostname == "" &&
              this.addNodeData.role == "source"
            ) {
              alert("当前role为‘source’,ap主机名是必填项！");
              return;
            }
            // console.log(this.addNodeData);
            // this.$axios({
            //   url: `${window.$config.HOST}/api/sink_source/registry`,
            //   method: "post",
            //   data: this.addNodeData, // body参数
            // })
            this.$axios
              .post(
                `${window.$config.HOST}/api/sink_source/registry`,
                this.addNodeData
              )
              .then((response) => {
                if (response.data.status == "OK") {
                  alert("增加成功！");
                  this.getTopoAndTableData(); // 刷新数据
                  // 清空新增数据信息
                  this.addNodeData = {
                    name: "",
                    role: "",
                    network_id: "",
                    source_info: "",
                    source_data_system: "",
                    ap_hostname: "",
                    description: "", // 可选
                    docker_port: "", // 可选
                  };
                  this.AddNodePageVisible = false; // 增加成功时才退了这个对话框
                } else {
                  alert("增加失败!");
                  console.log(response);
                }
              })
              .catch((error) => {
                console.log(error);
                alert("增加失败，前后端通信错误");
              });
          } else {
            alert("请填满相关内容");
            // console.log('error submit!!');
            return false;
          }
        });
      },

      indexSelect() {
        // console.log(this.edge_enum_choose);
        this.getTopoAndTableData();
      },
      async getTopoAndTableData() {
        const _this = this;
        await this.$axios
          .get(`${window.$config.HOST}/api/sink_source/topo`)
          .then((response) => {
            // alert('begin to get Topo');
            _this.data2 = response.data.data.nodes;
            _this.edges2 = response.data.data.edges;

            var optionOfTopo = {
              title: {
                show: true,
                text: "系统拓扑图",
                subtext: "source和sink节点",
                left: "auto",
                top: "auto",
              },
              grid: {
                top: "14%",
                bottom: "18%",
                left: "15%",
                right: "4%",
              },
              legend: [
                {
                  selectedMode: "single",
                  // data: categories.map(function (a) {
                  //   return a.name;
                  // })
                },
              ],
              animationDuration: 2000,
              coordinateSystem: "none",
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
                  zoom: 0.6, // 缩放比例
                  type: "graph",
                  layout: "circular", // "force"
                  name: "source or sink",

                  circular: {
                    rotateLabel: true,
                  },
                  symbolSize: 30, //  节点大小
                  // edgeSymbol: ['circle', 'arrow'],
                  animation: true,
                  data: _this.data2,
                  edges: _this.edges2,

                  // 效果不明
                  // force: {
                  //   // repulsion: 200,
                  //   edgeLength: 300,
                  //   repulsion: 4,
                  //   gravity: 19,
                  //   layoutAnimation: true,
                  //   friction: 100
                  // },
                  edgeSymbolSize: 120,

                  focusNodeAdjacency: 1,
                  itemStyle: {
                    // 点周围的阴影
                    borderColor: "#ffff",
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: "rgba(0, 0, 0, 0.6)",
                  },
                  roam: true,
                  label: {
                    position: "right",
                    formatter: "{b}",
                    fontStyle: "oblique",
                    fontWeight: "bolder",
                    fontFamily: "Segoe Print",
                    color: "rgba(50, 15, 15, 1)",
                    fontSize: 20, // 标签的字体大小
                  },
                  lineStyle: {
                    color: "rgba(205, 130, 130, 30)",
                    curveness: 0.4,
                    width: 4,
                    type: "solid",
                    shadowBlur: 1,
                  },
                  emphasis: {
                    lineStyle: {
                      width: 10,
                    },
                  },
                },
              ],
            };
            // _this.data2.symbolSize=50;
            var theTopoChart = echarts.init(document.getElementById("tpc"));
            theTopoChart.setOption(optionOfTopo, true);
            // console.log(_this.edges2);
            // console.log(_this.data2);
            // alert('goodTopo');
          })
          .catch((error) => {
            console.log(error);
            alert("sink-source系统topo数据获取失败，前后端通信错误");
          });

        await this.$axios
          .get(`${window.$config.HOST}/api/sink_source/list`, {
            params: {
              role: this.edge_enum_choose, // 必需
            },
          })
          .then((response) => {
            _this.tableData = response.data.data;
            // console.log(_this.tableData);
            // alert('goodTableData')
          })
          .catch((error) => {
            console.log(error);
            alert("sink-source系统表格数据获取失败，前后端通信错误");
          });
      },
    },

    mounted() {
      const that = this;
      this.getTopoAndTableData();
    },
  };
</script>

<style>
</style>