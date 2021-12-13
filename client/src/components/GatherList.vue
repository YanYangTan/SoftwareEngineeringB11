<template>
  <div>
    <el-button  @click="dialogFormVisible = true">打开嵌套表单的 Dialog</el-button>

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
    <el-dialog :title="this.gatheringdialogtitle" :visible.sync="voteFormVisible">
      <el-table
    :data="this.contents.options"
    style="width: 100%"
      v-loading="loading">
        <el-table-column
      label="截止日期"
      prop="content.time">
    </el-table-column>
        <el-table-column
      label="场所"
      prop="content.location">
    </el-table-column>
        <el-table-column
      label="投票数"
      prop="vote_count">
    </el-table-column>
        <el-table-column
        prop="voted">
<!-- ---------------------------- vote ------------------------------------------------------------>
<!--       <div v-if="this.gatheringdialogtitle==='投票'">-->
          <template slot="header" slot-scope={}>
<el-checkbox :indeterminate="isIndeterminate">全选</el-checkbox>
      </template>
      <template slot-scope="scope">
    <el-checkbox @change="changeIt()" v-model="scope.row.voted">投票</el-checkbox>
      </template></el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
    <el-button @click="voteFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirmVote">{{this.gatheringdialogtitle}}</el-button>
  </div>
    </el-dialog>
<!--                </div>-->
<!-- ---------------------------- tiyi ------------------------------------------------------------>

    <el-dialog :title="this.gatheringdialogtitle" :visible.sync="suggestionFormVisible">
      <el-table
    :data="this.contents.options"
    style="width: 100%"
      v-loading="loading">
        <el-table-column
      label="截止日期"
      prop="content.time">
    </el-table-column>
        <el-table-column
      label="场所"
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
<!--    -->
    <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/>
    <el-card>
  <el-table
    :data="this.gatherlist.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%"
  v-loading="loading">
    <el-table-column
      label="截止日期"
      prop="enddate">
    </el-table-column>
    <el-table-column
      label="名字"
    prop="name">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top-start" >
          <p>描述: {{ scope.row.description }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag type='info' size="medium">{{ scope.row.name }}</el-tag>
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
      width="100"
      :filters="[{ text: '投票', value: false }, { text: '提议', value: true }]"
      :filter-method="filterTag"
      filter-placement="bottom-end">
      <template slot-scope="scope">
        <el-tag @click="tagClickedSuggestion(scope.row)"
          type='primary'
          v-if="scope.row.status " >提议</el-tag>
        <el-tag @click="tagClickedVote(scope.row)"
          type='warning'
          v-else-if="scope.row.status === false && scope.row.voted" >已投票</el-tag>
        <el-tag @click="tagClickedVote(scope.row)"
          type='success'
          v-else-if="scope.row.status === false && scope.row.voted===false" >投票</el-tag>
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
      loading: true,
      gatherlist: [],
      contents: {},
      addingcontent: false,
      dialogFormVisible: false,
      voteFormVisible: false,
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
      axios.post('/api/query-all-gathering', { group_id: this.$props.currentgroup.id })
        .then((res) => {
          if (res.data.status) {
            this.gatherlist = res.data.gathering_list;
            // eslint-disable-next-line no-restricted-syntax
            for (const item of this.gatherlist) {
              axios.post('/api/check-vote', { user_id: this.$route.params.userid, gathering_id: item.id })
              // eslint-disable-next-line consistent-return
                .then((res2) => {
                  if (res2.data.status) {
                    item.voted = res2.data.voted;
                  } else {
                    item.voted = false;
                  }
                })
                .catch((err) => {
                  console.log(err);
                });
            }
            this.loading = false;
            console.log(this.gatherlist);
          }
        })
        .catch((err) => {
          console.log(err);
        });
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
          if (res.data.status) {
            this.gatherlist = res.data.gathering_list;
            // appendTag();
            this.queryAllGathering();
          } else {
            console.log(res.data.status);
          }
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
    confirmVote() {
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
      console.log(this.contents);
    },
    tagClickedVote(row) {
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
                    this.voteFormVisible = true;
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
  },
  mounted() {
    this.queryAllGathering();
  },
  created() {
    this.queryAllGathering();
  },
};
</script>
