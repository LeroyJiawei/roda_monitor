<template>
  <div class="container">
    <el-card class="box-card">
      <div class="head">
        <h1 class="title" style="display: inline-block">私有仓库信息</h1>
        <el-tag class="info-tag" type="success" effect="dark">
          IP地址:{{ hub_info.addr }}
        </el-tag>
        <el-tag class="info-tag" type="warning" effect="dark">
          端口:{{ hub_info.port }}
        </el-tag>
        <el-tag type="info"> DOKCER端口:{{ hub_info.docker_port }} </el-tag>
      </div>
    </el-card>

    <el-card class="box-card">
      <div class="image-manager">
        <h1 class="title">辅助文件管理</h1>
        <el-upload
          style="margin: 10px"
          :action="tarUploadUrl"
          :limit="1"
          :on-exceed="handleExceed"
          :file-list="tarFileList"
          :on-error="uploadFailed"
          :on-success="uploadSuccess"
        >
          <el-button size="small" type="primary">上传文件</el-button>
        </el-upload>

        <el-table
          :data="fileTableData"
          stripe
          style="width: 98%; margin-left: 10px"
        >
          <el-table-column prop="name" label="Tar包名"> </el-table-column>
          <el-table-column prop="url" label="资源路径"> </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="deleteFile(scope.$index, fileTableData)"
                type="danger"
                size="small"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <el-card class="box-card">
      <div class="image-manager">
        <h1 class="title">Image管理</h1>
        <el-button
          type="primary"
          style="margin: 10px"
          @click="buildImageClick()"
          >新增</el-button
        >
        <el-table
          :data="tableData"
          style="width: 98%; margin-left: 10px"
          max-height="250"
        >
          <el-table-column prop="name" label="名称"> </el-table-column>
          <el-table-column prop="tag" label="标签"> </el-table-column>

          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="deleteRow(scope.$index, tableData)"
                type="danger"
                size="small"
              >
                删除
              </el-button>

              <el-button
                @click.native.prevent="deployClick(scope.$index, tableData)"
                type="primary"
                size="small"
              >
                部署
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <el-dialog
      title="请输入部署节点的信息："
      :visible.sync="deployDialogVisible"
      center
      :append-to-body="0"
      :lock-scroll="true"
      width="100%"
      :modal-append-to-body="false"
      :before-close="handleDeployDialogClose"
    >
      <el-form
        :model="deployData"
        status-icon
        ref="deployData"
        label-width="200px"
        :rules="rulesOfDeployNode"
      >
        <el-form-item label="源系统" prop="deploySourceId">
          <el-select v-model="deployData.deploySourceId" placeholder="请选择">
            <el-option
              v-for="item in deploySourceOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="目的系统" prop="deploySinkId">
          <el-select v-model="deployData.deploySinkId" placeholder="请选择">
            <el-option
              v-for="item in deploySinkOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Base Rate" prop="deployBaseRate">
          <el-input
            v-model.number="deployData.deployBaseRate"
            placeholder="请输入"
          >
          </el-input>
        </el-form-item>

        <el-form-item label="最大线程数" prop="deployMaxThread">
          <el-input
            v-model.number="deployData.deployMaxThread"
            placeholder="请输入"
          >
          </el-input>
        </el-form-item>

        <el-form-item label="匹配阈值" prop="deployMatchExp">
          <el-input
            v-model.number="deployData.deployMatchExp"
            placeholder="请输入"
          >
          </el-input>
        </el-form-item>

        <el-form-item label="统计窗口大小" prop="deployWinSize">
          <el-input
            v-model.number="deployData.deployWinSize"
            placeholder="请输入"
          >
          </el-input>
        </el-form-item>
      </el-form>

      <el-row
        type="flex"
        justify="center"
        class="dialog-row"
        style="margin: 20px"
      >
        <el-col :span="4">
          <el-button @click="handleDeployDialogClose()">
            <span style="font-size: 15px"> 取 消 </span>
          </el-button>
        </el-col>

        <el-col :span="4">
          <el-button
            type="primary"
            @click="handleDeployDialogSure('deployData')"
          >
            <span style="font-size: 15px"> 确定</span>
          </el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <el-dialog
      title="构建镜像"
      :visible.sync="buildImageDialogVisible"
      center
      :append-to-body="0"
      :lock-scroll="true"
      width="100%"
      :modal-append-to-body="false"
      :before-close="handleBuildImageDialogClose"
    >
      <el-row type="flex" justify="center" class="dialog-row">
        <el-col :span="4">
          <span class="row-span">镜像名称：</span>
        </el-col>
        <el-col :span="6">
          <el-input v-model="hub_info.new_image_name" placeholder="请输入">
          </el-input>
        </el-col>
      </el-row>

      <el-row type="flex" justify="center" class="dialog-row">
        <el-col :span="4">
          <span class="row-span">镜像标签：</span>
        </el-col>
        <el-col :span="6">
          <el-input v-model="hub_info.new_image_tag" placeholder="请输入">
          </el-input>
        </el-col>
      </el-row>

      <el-row
        type="flex"
        justify="center"
        class="dialog-row"
        style="margin: 20px"
      >
        <el-col :span="4">
          <el-upload
            :action="dockerFileUploadUrl"
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="dockerFileList"
            :on-error="uploadFailed"
            :data="hub_info"
            :before-upload="dockerFileCheck"
          >
            <el-button size="small" type="primary">
              <span style="font-size: 20px">上传dockerfile</span>
            </el-button>
          </el-upload>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hub_info: {
        addr: "",
        port: "",
        new_image_name: "",
        new_image_tag: "",
      },
      tableData: [],

      buildImageDialogVisible: false,
      fileTableData: [],
      tarFileList: [],
      dockerFileList: [],
      tarUploadUrl: `${window.$config.HOST}/api/hub/upload_file`,
      dockerFileUploadUrl: `${window.$config.HOST}/api/hub/upload_dockerfile`,

      rulesOfDeployNode: {
        deploySourceId: [{ required: true, message: "不能为空" }],
        deploySinkId: [{ required: true, message: "不能为空" }],
        deployBaseRate: [
          { required: true, message: "不能为空" },
          { type: "float", message: "范围：0～1" },
        ],
        deployMaxThread: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" },
        ],
        deployMatchExp: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" },
        ],
        deployWinSize: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" },
        ],
      },

      deployDialogVisible: false,
      deployImage: {
        name: "",
        tag: "",
      },
      deploySourceOptions: [],
      deploySinkOptions: [],
      deployData: {
        deploySourceId: null,
        deploySinkId: null,
        deployBaseRate: null,
        deployMaxThread: null,
        deployMatchExp: null,
        deployWinSize: null,
      },
    };
  },
  methods: {
    getTarData() {
      this.$axios
        .get(`${window.$config.HOST}/api/hub/list_file`)
        .then((response) => {
          if (response.data.status == "OK") {
            this.fileTableData = response.data.data;
          } else {
            this.$message.error({
              message: "获取辅助文件信息失败：" + response.data.status,
            });
          }
        })
        .catch((error) => {
          this.$message.error({
            message: "获取辅助文件信息失败" + error,
          });
        });
    },
    buildImageClick() {
      this.buildImageDialogVisible = true;
    },

    handleBuildImageDialogClose() {
      this.hub_info.new_image_name = undefined;
      this.hub_info.new_image_tag = undefined;

      this.buildImageDialogVisible = false;
      this.getHubInfoAndImages();
      this.dockerFileList = [];
    },

    uploadSuccess(response, file, fileList) {
      this.hub_info.new_image_name = undefined;
      this.hub_info.new_image_tag = undefined;
      this.getTarData();
      console.log(fileList);
      while (fileList.length > 1) {
        fileList.shift();
      }
    },

    uploadFailed(err, file, fileList) {
      console.log(err);
      this.$message.error({
        message: "上传失败",
      });
    },

    dockerFileCheck(file) {
      if (!this.hub_info.new_image_name) {
        this.$message.error("请输入新镜像名称和标签");
        return false;
      }
    },

    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${
          files.length + fileList.length
        } 个文件`
      );
    },

    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    deleteFile(index, fileTableData) {
      this.$axios({
        url: `${window.$config.HOST}/api/hub/delete_file`,
        method: "delete",
        data: {
          file_name: this.fileTableData[index].name,
        }, // body参数
      })
        .then((response) => {
          // console.log(response);
          if (response.data.status == "OK") {
            this.$message({
              message: "删除文件成功!",
            });
            this.getTarData();
          } else {
            this.$message.error({
              message: "删除文件失败：" + response.data.status,
            });
            console.log(response);
          }
        })
        .catch((error) => {
          this.$message.error({
            message: "删除文件失败，前后端通信错误",
          });
          console.log(error);
        });
    },

    async getHubInfoAndImages() {
      await this.$axios
        .get(`${window.$config.HOST}/api/hub/info`)
        .then((response) => {
          if (response.data.status != "OK") {
            this.$message.error({
              message: "镜像仓库信息获取失败：" + response.data.status,
            });
          } else {
            this.hub_info = response.data.data;
          }
        })
        .catch((error) => {
          this.$message.error({
            message: "镜像仓库信息获取失败,通信错误！" + error,
          });
        });

      await this.$axios
        .get(`${window.$config.HOST}/api/hub/list_images`)
        .then((response) => {
          if (response.data.status != "OK") {
            this.$message.error({
              message: "Images信息获取失败：" + response.data.status,
            });
            console.log(response);
          } else this.tableData = response.data.data;
        })
        .catch((error) => {
          console.log(error);
          this.$message.error({
            message: "Images信息获取失败,通信错误",
          });
        });
    },

    deleteRow(index, rows) {
      // rows.splice(index, 1);
      console.log(this.tableData[index]);
      this.$axios({
        url: `${window.$config.HOST}/api/hub/delete_image`,
        method: "delete",
        data: {
          name: this.tableData[index].name,
          tag: this.tableData[index].tag,
          hub_addr: this.hub_info.addr,
          hub_port: this.hub_info.port,
        }, // body参数
      })
        .then((response) => {
          // console.log(response);
          if (response.data.status == "OK") {
            this.$message({
              message: "删除成功",
            });
            this.getHubInfoAndImages();
          } else {
            this.$message.error({
              message: "删除失败：" + response.data.status,
            });
          }
        })
        .catch((error) => {
          this.$message.error({
            message: "删除失败：" + error,
          });
          console.log(error);
        });
    },

    deployClick(index, tableData) {
      var row = tableData[index];
      this.deployImage.name = row.name;
      this.deployImage.tag = row.tag;

      this.$axios
        .get(`${window.$config.HOST}/api/sink_source/list`, {
          params: {
            role: "all",
          },
        })
        .then((response) => {
          if (response.data.status == "OK") {
            this.deploySourceOptions = [];
            this.deploySinkOptions = [];
            response.data.data.forEach((element) => {
              if (element.role == "source") {
                this.deploySourceOptions.push(element);
              } else {
                this.deploySinkOptions.push(element);
              }
            });
          } else {
            console.log("源系统信息获取出错");
          }
        })
        .catch((error) => {
          console.log(error);
          this.$message.error({
            message: "网络页面的表格数据获取失败,通信错误",
          });
        });
      this.deployDialogVisible = true;
    },

    handleDeployDialogClose() {
      this.deployImage.name = null;
      this.deployImage.tag = null;
      this.deployDialogVisible = false;
    },

    handleDeployDialogSure(formName) {
      this.$refs[formName].validate((valid) => {
        console.log(this.deployData.deploySourceId, sourceInfo, sinkInfo);

        if (valid) {
          var sourceInfo, sinkInfo;
          this.deploySourceOptions.forEach((ele) => {
            if (ele.id === this.deployData.deploySourceId) {
              sourceInfo = ele.source_info;
            }
          });
          this.deploySinkOptions.forEach((ele) => {
            if (ele.id === this.deployData.deploySinkId) {
              sinkInfo = ele.source_info;
            }
          });
          this.$axios
            .post(`${window.$config.HOST}/api/hub/run_image`, {
              target_id: this.deployData.deploySourceId,
              image_name: this.deployImage.name,
              image_tag: this.deployImage.tag,
              source_info: sourceInfo,
              sink_info: sinkInfo,
              max_attr: 60,
              win_size: this.deployData.deployWinSize,
              match_threshold: this.deployData.deployMatchExp,
              max_thread: this.deployData.deployMaxThread,
              base_rate: this.deployData.deployBaseRate,
            })
            .then((response) => {
              if (response.data.status == "OK") {
                this.$message({
                  message: "部署成功",
                });
                this.deployDialogVisible = false;
              } else {
                this.$message.error({
                  message: "部署失败:" + response.data.status,
                });
              }
            })
            .catch((error) => {
              this.$message.error({
                message: "部署失败:" + error,
              });
            });
        }
      });
    },
  },
  mounted() {
    this.getHubInfoAndImages();
    this.getTarData();
  },
};
</script>

<style scoped>
.box-card {
  width: 100%;
  margin: 0 auto 10px;
}

.text {
  font-size: 14px;
}

.item {
  padding: 18px 0;
}

.title {
  font-size: 24px;
  margin: 10px;
}

.el-tag {
  height: 35px;
  /* padding:10px; */
  line-height: 35px;
  font-size: 18px;
  margin-right: 10px;
}

.info-button {
  float: right;
  margin: 20px;
}

.dialog-row {
  margin: 0 0 5px;
}

.row-span {
  position: relative;

  font-size: 20px;
  position: relative;
  top: 10%;
  transform: translateY(-50%);
  justify-content: center; /* transform: translateY(-50%); */
}
</style>