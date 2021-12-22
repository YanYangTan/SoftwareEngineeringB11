<template>
  <div>
    <el-button  @click="dialogFormVisible = true" type="primary" icon="el-icon-circle-plus-outline
">发起新聚会</el-button>
     <el-button  @click="changeDateClick" type="primary" icon="el-icon-edit
">{{ChangeDateButton}}</el-button>
<el-button  @click="deleteClick" type="danger" icon="el-icon-delete
">{{DeleteButton}}</el-button>
<el-dialog title="发起聚会" :visible.sync="dialogFormVisible">
  <el-form :model="temp">
    <el-form-item label="聚会名称" :label-width="formLabelWidth">
      <el-input v-model="gathering.name" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="描述" :label-width="formLabelWidth">
      <el-input v-model="gathering.description" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="截止时间">
    <el-date-picker
      v-model="gathering.enddate"
      value-format="yyyy-MM-dd HH:mm:ss"
      type="datetime"
      placeholder="选择日期时间">
    </el-date-picker>
  </el-form-item>
    <el-form-item label="发起类型" :label-width="formLabelWidth">
      <el-radio-group v-model="gathering.status">
      <el-radio label="提议"></el-radio>
      <el-radio label="投票"></el-radio>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="投票多选" :label-width="formLabelWidth">
       <el-switch v-model="gathering.allow_multiple_vote"></el-switch>
    </el-form-item>
    <el-form-item label="内容" :label-width="formLabelWidth">
  <el-form-item
    v-for="(domain, index) in  gathering.content"
    :label="'方案 ' + index"
    :key="domain.key"
    :rules="{
      required: true, message: '不能为空', trigger: 'blur'
    }"
  >
    <el-col :span="11">
      <el-date-picker
      v-model="domain.time"
      type="datetime"
      value-format="yyyy-MM-dd HH:mm:ss"
      placeholder="选择日期时间">
    </el-date-picker>
    </el-col>
    <el-input v-model="domain.location"></el-input><el-button @click.prevent="removeDomain(domain)">删除</el-button>
  </el-form-item>
  <el-form-item>
    <el-button @click="addDomain">新建内容</el-button>
    <el-button @click="resetForm">重置</el-button>
  </el-form-item>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirmGathering">确 定</el-button>
  </div>
</el-dialog>
<!--    -->
    <!-- ---------------------------- vote ------------------------------------------------------------>
    <el-dialog :title="this.gatheringdialogtitle" :visible.sync="voteFormVisible">
      <el-table
    :data="this.contents.options"
    style="width: 100%"
      v-loading="loading">
        <el-table-column
      width="150px"
      label="日期"
      prop="content.time">
    </el-table-column>
        <el-table-column
      label="地点"
      prop="content.location">
    </el-table-column>
        <el-table-column
      label="投票数"
      prop="vote_count">
    </el-table-column>
        <el-table-column
          label="投票"
        prop="voted">
<!--       <div v-if="this.gatheringdialogtitle==='投票'">-->
<!--          <template slot="header" slot-scope={}>-->
<!--<el-checkbox :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选</el-checkbox>-->
<!--      </template>-->
      <template slot-scope="scope">
    <el-checkbox @change="changeIt(scope.$index)" v-model="scope.row.voted">投票</el-checkbox>
      </template></el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
    <el-button @click="voteFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirmVote">{{this.gatheringdialogtitle}}</el-button>
  </div>
    </el-dialog>
<!--                </div>-->
        <!-- ---------------------------- One vote ------------------------------------------------------------>
    <el-dialog :title="this.gatheringdialogtitle" :visible.sync="voteOneFormVisible">
      <el-table
    :data="this.contents.options"
    style="width: 100%"
      v-loading="loading">
        <el-table-column
      width="150px"
      label="日期"
      prop="content.time">
    </el-table-column>
        <el-table-column
      label="地点"
      prop="content.location">
    </el-table-column>
        <el-table-column
      label="投票数"
      prop="vote_count">
    </el-table-column>
        <el-table-column
          label="投票"
        prop="voted">
<!--       <div v-if="this.gatheringdialogtitle==='投票'">-->
<!--          <template slot="header" slot-scope={}>-->
<!--<el-checkbox :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选</el-checkbox>-->
<!--      </template>-->
      <template slot-scope="scope">
        <el-button type="primary" @click="VoteOne(scope.row)">投票</el-button>
<!--    <el-checkbox @change="changeIt(scope.$index)" v-model="scope.row.voted">投票</el-checkbox>-->
      </template></el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
    <el-button @click="voteFormVisible = false">取 消</el-button>
<!--    <el-button type="primary" @click="confirmVote">{{this.gatheringdialogtitle}}</el-button>-->
  </div>
    </el-dialog>
<!-- ---------------------------- tiyi ------------------------------------------------------------>

    <el-dialog :title="this.gatheringdialogtitle" :visible.sync="suggestionFormVisible">
      <el-table
    :data="this.contents.options"
    style="width: 100%"
    ref="multipleTable"
      v-loading="loading">
        <el-table-column
          width="150px"
      label="日期"
      prop="content.time">
    </el-table-column>
        <el-table-column
          width="220px"
      label="地点"
      prop="content.location">
    </el-table-column>
        <el-table-column
      label="提议人"
      prop="username">
    </el-table-column>
        <el-table-column
        prop="voted">
        </el-table-column>
      </el-table>
      <div v-if="this.gatheringdialogtitle==='提议'" >
          <el-form :model="temp">
        <el-form-item label="内容" :label-width="formLabelWidth">
  <el-form-item
    v-for="(domain, index) in  gathering.content"
    :label="'方案 ' + index"
    :key="domain.key"
    :rules="{
      required: true, message: '不能为空', trigger: 'blur'
    }"
  >
    <el-col :span="11">
      <el-date-picker
      v-model="domain.time"
      type="datetime"
      value-format="yyyy-MM-dd HH:mm:ss"
      placeholder="选择日期时间">
    </el-date-picker>
    </el-col>
    <el-input v-model="domain.location"></el-input><el-button @click.prevent="removeDomain(domain)">删除</el-button>
  </el-form-item>
  <el-form-item>
    <el-button @click="addDomain">新建内容</el-button>
    <el-button @click="resetForm">重置</el-button>
  </el-form-item>
    </el-form-item>
          </el-form>
          </div>
      <div slot="footer" class="dialog-footer">
    <el-button @click="suggestionFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirmContent">{{this.gatheringdialogtitle}}</el-button>
  </div>
    </el-dialog>
    <!-- ---------------------------- changedate------------------------------------------------------------>
     <el-dialog title="更改截止日期" :visible.sync="ChangeDateDialogVisible">
       <el-form>
  <el-form-item label="选择新的截至日期">
      <el-date-picker
      v-model="changedatetime"
      type="datetime"
      value-format="yyyy-MM-dd HH:mm:ss"
      placeholder="选择日期时间">
    </el-date-picker>
    </el-form-item>
       </el-form>
      <div slot="footer" >
    <el-button @click="ChangeDateDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirmChangeDate">设置</el-button>
  </div>
    </el-dialog>
    <!-- ---------------------------- table ------------------------------------------------------------>
<!--    -->
    <el-container style="margin-top: 10px;margin-bottom: 10px">
    <label style="width: 75px">搜索聚会:</label>
    <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/></el-container>
    <el-card>
  <el-table
    ref="TableGather"
    :data="this.gatherlist.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%"
  v-loading="loading">
    <el-table-column
      width="400px"
      label="截止日期"
      prop="enddate">
      <template slot-scope="scope">
        <span>{{scope.row.enddate}}</span>
      <el-button @click="ChangeDateClick(scope.row)"
                 style="margin-left: 10px"
                   size="mini"
                 icon="el-icon-edit"
          type='warning'
          v-if="matchStateDate(scope.row)" ></el-button>
      </template>
    </el-table-column>
    <el-table-column
      label="名字"
    prop="name">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top-start" >
          <p>描述: {{ scope.row.description }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag type='info' size="medium">{{ scope.row.name }}</el-tag>
            <el-button @click="DeleteClick(scope.$index,scope.row)"
                       style="margin-left: 10px"
                   size="mini" type='danger' icon="el-icon-delete"
          v-if="matchStateDeleted(scope.row)" ></el-button>
          </div>
        </el-popover>
      </template>
    </el-table-column>
<!--    <el-table-column-->
<!--      align="right">-->
<!--      <template slot="header" slot-scope={}>-->
<!--      </template>-->
<!--    </el-table-column>-->
    <el-table-column
      prop="status"
      label="标签"
      width="170px"
      :filters="[{ text: '投票', value: false }, { text: '提议', value: true }]"
      :filter-method="filterTag"
      filter-placement="bottom-end">
      <template slot-scope="scope">
        <el-tag @click="tagClickedSuggestion(scope.row)"
          type='primary'
          v-if="scope.row.status " >提议</el-tag>
        <el-tag @click="tagClickedVote(scope.row)"
          type='warning'
          v-else-if="matchStateVoted(scope.row)" >已投票</el-tag>
        <el-tag @click="tagClickedVote(scope.row)"
          type='success'
          v-else-if="matchState(scope.row)" >投票</el-tag>
      </template>
    </el-table-column>
  </el-table>
      </el-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      changedatetimeRow: {},
      changedatetime: '2021-12-31 00:00:00',
      ChangeDateVisible: false,
      ChangeDateDialogVisible: false,
      ChangeDateButton: '更改截止日期',
      DeleteButton: '删除聚会',
      DeleteVisible: false,
      isIndeterminate: true,
      loading: true,
      gatherlist: [],
      contents: {},
      addingcontent: false,
      dialogFormVisible: false,
      voteFormVisible: false,
      voteOneFormVisible: false,
      suggestionFormVisible: false,
      check: true,
      gathering: {
        user_id: '',
        group_id: '',
        name: '',
        description: '',
        enddate: '',
        status: '提议',
        allow_multiple_vote: 0,
        content: [{ time: '', location: '' }],
      },
      temp: {
        name: '',
        region: '',
        enddateday: '',
        enddatetime: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
      },
      gatheringdialogtitle: '',
      currentgathering: {},
      isvoted: false,
      formLabelWidth: '120px',
      search: '',
      submitsuggest: {},
    };
  },
  props: {
    currentgroup: {},
  },
  methods: {
    matchStateDate(row) {
      return this.ChangeDateVisible && (Number(row.user_id) === Number(this.$route.params.userid));
    },
    changeDateClick() {
      if (this.ChangeDateVisible === true) {
        this.ChangeDateVisible = false;
        this.ChangeDateButton = '更改截止日期';
      } else {
        this.ChangeDateVisible = true;
        this.ChangeDateButton = '更改完毕';
      }
    },
    confirmChangeDate() {
      this.ChangeDateDialogVisible = false;
      axios.post('/api/change-enddate', { gathering_id: this.changedatetimeRow.id, new_date: this.changedatetime })
      // eslint-disable-next-line consistent-return
        .then((res) => {
          if (res.data.status) {
            this.$message({
              type: 'success',
              message: '更改日期成功',
            });
            this.queryAllGathering();
          } else {
            this.$message({
              type: 'warning',
              message: `更改失败 ${res.data.message}`,
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    ChangeDateClick(row) {
      this.ChangeDateDialogVisible = true;
      this.changedatetimeRow = row;
    },
    DeleteClick(index, row) {
      // console.log(row.user_id === this.$route.params.userid);
      axios.post('/api/delete-gathering', { user_id: Number(this.$route.params.userid), gathering_id: row.id })
      // eslint-disable-next-line consistent-return
        .then((res) => {
          if (res.data.status) {
            this.$data.gatherlist.splice(index, 1);
            this.$message({
              type: 'success',
              message: '成功删除聚会',
            });
          } else {
            this.$message({
              type: 'warning',
              message: `删除聚会失败 ${res.data.message}`,
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    deleteClick() {
      if (this.DeleteVisible === true) {
        this.DeleteVisible = false;
        this.DeleteButton = '删除聚会';
      } else {
        this.DeleteVisible = true;
        this.DeleteButton = '删除完毕';
      }
    },
    matchStateDeleted(row) {
      return this.DeleteVisible && (Number(row.user_id) === Number(this.$route.params.userid));
    },
    matchStateVoted(row) {
      return row.status === false && row.voted;
    },
    matchState(row) {
      return row.status === false && row.voted === false;
    },
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    filterTag(value, row) {
      return row.status === value;
    },
    queryAllGathering() {
      this.loading = true;
      axios.post('/api/query-all-gathering', { group_id: this.$props.currentgroup.id, user_id: this.$route.params.userid })
        .then((res) => {
          if (res.data.status) {
            this.gatherlist = res.data.gathering_list;

            // eslint-disable-next-line no-restricted-syntax
            // for (const item of this.gatherlist) {
            //   if (item.status === false) {
            //     axios.post('/api/check-vote', { user_id: this.$route.params.userid, gathering_id: item.id })
            //     // eslint-disable-next-line consistent-return
            //       .then((res2) => {
            //         if (res2.data.status) {
            //           item.voted = res2.data.voted;
            //         } else {
            //           item.voted = false;
            //         }
            //       })
            //       .catch((err) => {
            //         console.log(err);
            //       });
            //   }
            // }
            // this.$refs.TableGather.doLayout();
            this.loading = false;
            console.log(this.gatherlist);
          }
          //   this.gatherlist = res.data.gathering_list;
          //   // eslint-disable-next-line no-restricted-syntax,guard-for-in
          //   for (const item of this.gatherlist) {
          //     console.log(item);
          //     axios.post('/api/check-vote', { user_id: this.$route.params.userid, gathering_id: item.id })
          //       // eslint-disable-next-line consistent-return
          //       .then((res2) => {
          //         if (res2.data.status) {
          //           this.item.voted = res2.data.voted;
          //           console.log(this.item);
          //         } else {
          //           this.item.voted = false;
          //         }
          //       })
          //       .catch((err) => {
          //         console.log(err);
          //       });
          //   }
          //   // this.gatherlist = res.data.gathering_list;
          //   this.loading = false;
          //   console.log(this.gatherlist);
          // }
        })
        .catch((err) => {
          console.log(err);
        });
      // this.$refs.TableGather.doLayout();
    },
    addContent() {
      this.addingcontent = true;
    },
    // 内容
    resetForm() {
      this.gathering.content = [{ time: '', location: '' }];
    },
    removeDomain(item) {
      const index = this.gathering.content.indexOf(item);
      if (index !== -1) {
        this.gathering.content.splice(index, 1);
      }
    },
    addDomain() {
      this.gathering.content.push({
        time: '',
        location: '',
        key: Date.now(),
      });
    },
    confirmGathering() {
      this.dialogFormVisible = false;
      this.gathering.group_id = this.$props.currentgroup.id;
      this.gathering.user_id = this.$route.params.userid;
      this.gathering.status = this.gathering.status === '提议';
      // this.gathering.status = '1';
      console.log(this.gathering);
      axios.post('/api/create-gathering', {
        user_id: this.gathering.user_id,
        group_id: this.gathering.group_id,
        name: this.gathering.name,
        description: this.gathering.description,
        enddate: this.gathering.enddate,
        status: this.gathering.status,
        allow_multiple_vote: this.gathering.allow_multiple_vote,
        content: this.gathering.content,
      })
        .then((res) => {
          let messagetype;
          let str;
          if (res.data.status) {
            this.gatherlist = res.data.gathering_list;
            // appendTag();
            messagetype = 'success';
            str = '成功发起聚会';
            this.queryAllGathering();
          } else {
            messagetype = 'warning';
            str = '发起聚会失败';
            console.log(res.data.status);
          }
          this.$message({
            type: messagetype,
            message: str,
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    confirmContent() {
      this.gathering.user_id = this.$route.params.userid;
      // this.contents.options.push(this.gathering.content);
      // eslint-disable-next-line no-restricted-syntax
      for (const item of this.contents.options) {
        this.gathering.content.push(item.content);
      }
      axios.post('/api/save-suggestion', {
        gathering_id: this.currentgathering.id,
        user_id: this.gathering.user_id,
        content: this.gathering.content,
      })
        .then((res) => {
          if (res.data.status) {
            console.log(res.data.message);
            // this.tagClickedSuggestion(this.currentgathering);
            this.suggestionFormVisible = false;
          }
        })
        .catch((err) => {
          console.log(err);
        });
      this.gathering.content = [];
    },
    VoteOne(row) {
      axios.post('/api/vote', { vote_ids: [row.id], user_id: this.$route.params.userid })
        .then((res) => {
          if (res.data.status) {
            console.log(res.data.message);
            this.currentgathering.voted = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
      this.voteOneFormVisible = false;
    },
    confirmVote() {
      this.voteFormVisible = false;
      const votecontent = { vote_ids: [], user_id: 0 };
      votecontent.user_id = this.$route.params.userid;
      // eslint-disable-next-line no-restricted-syntax
      for (const item of this.contents.options) {
        if (item.voted === true) {
          votecontent.vote_ids.push(item.id);
        }
      }
      if (votecontent.vote_ids.length !== 0) {
        axios.post('/api/vote', { vote_ids: votecontent.vote_ids, user_id: votecontent.user_id })
          .then((res) => {
            if (res.data.status) {
              console.log(res.data.message);
              this.currentgathering.voted = true;
            }
          })
          .catch((err) => {
            console.log(err);
          });
        console.log(votecontent);
      } else {
        this.$message({
          type: 'warning',
          message: '未选择选项',
        });
      }
    },
    changeIt() {
      // if (!this.contents.allow_multiple_vote) {
      //   console.log(this.contents.options[index].voted);
      //   if (this.contents.options[index].voted === true) {
      //     console.log('asdasd');
      //     // eslint-disable-next-line guard-for-in,no-restricted-syntax
      //     for (const x in this.contents.options) {
      //       this.contents.options[x].voted = false;
      //     }
      //     this.contents.options[index].voted = true;
      //   }
      // }
    },
    tagClickedVote(row) {
      this.contents = {};
      console.log(row);
      axios.post('/api/check-vote', { user_id: this.$route.params.userid, gathering_id: row.id })
        // eslint-disable-next-line consistent-return
        .then((res) => {
          if (res.data.status) {
            this.isvoted = res.data.voted;
            if (this.isvoted === true) {
              this.$message({
                type: 'warning',
                message: '你已投票',
              });
            } else {
              this.loading = true;
              axios.post('/api/query-gathering', { gathering_id: row.id })
                .then((res1) => {
                  this.loading = false;
                  if (res1.data.status) {
                    this.contents = res1.data;
                    console.log(this.contents);
                    this.currentgathering = row;
                    if (res1.data.allow_multiple_vote) {
                      this.voteFormVisible = true;
                    } else {
                      this.voteOneFormVisible = true;
                    }
                    this.gatheringdialogtitle = '投票';
                  }
                })
                .catch((err) => {
                  console.log(err);
                });
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    tagClickedSuggestion(row) {
      this.resetForm();
      this.loading = true;
      axios.post('/api/query-gathering', { gathering_id: row.id })
        .then((res) => {
          this.loading = false;
          if (res.data.status) {
            this.contents = res.data;
            console.log(this.contents);
            this.currentgathering = row;
            this.suggestionFormVisible = true;
            this.gatheringdialogtitle = '提议';
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    checkVoted(gathering) {
      axios.post('/api/check-vote', { user_id: this.$route.params.userid, gathering_id: gathering.id })
        // eslint-disable-next-line consistent-return
        .then((res) => {
          if (res.data.status) {
            this.isvoted = res.data.voted;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // handleCheckAllChange(val) {
    //   if (val) {
    //     // eslint-disable-next-line no-restricted-syntax
    //     for (const item of this.contents.options) {
    //       item.voted = true;
    //     }
    //     console.log(this.contents.options);
    //     this.isIndeterminate = false;
    //   } else {
    //     // eslint-disable-next-line no-restricted-syntax
    //     for (const item of this.contents.options) {
    //       item.voted = false;
    //     }
    //     this.isIndeterminate = true;
    //   }
    // },
  },
  mounted() {
    this.queryAllGathering();
    // this.$refs.TableGather.doLayout();
  },
  created() {
    this.queryAllGathering();
  },
};
</script>
