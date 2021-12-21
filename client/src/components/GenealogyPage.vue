<template>
  <div id="app">
    <el-card>
<!--    <div class="text-center">-->
<!--&lt;!&ndash;      <h1 class="title">家谱</h1>&ndash;&gt;-->
<!--    </div>-->
    <VueFamilyTree
      :tree="tree"
      @card-click="cardClick"
    >
      <template
        v-if="customCard"
        v-slot:card="{item}"
      >
        <el-popover
  placement="right"
  width="100"
  trigger="click">
  <el-menu :default-openeds="['2']">
    <el-menu-item index="2-1" @click="cardClick(item)">查看信息</el-menu-item>
    <el-popover
  placement="right"
  width="100"
  trigger="click">
      <el-menu :default-openeds="['3']">
        <el-menu-item index="3-1" @click="addMember(item,'Sibling')">兄弟</el-menu-item>
        <el-menu-item index="2-2" @click="addMember(item,'Children')">儿女</el-menu-item>
        <el-menu-item index="2-2" @click="addMember(item,'Honey')">配偶</el-menu-item>
      </el-menu>
    <el-menu-item slot="reference" index="2-2" @click="cardClick(item)">添加成员</el-menu-item>
    </el-popover>
  </el-menu>
        <el-button slot="reference" class="custom-card"  @click="cardClick(item)">
          <div
            :style="{backgroundImage: item.image ? `url(${item.image})` :  null}"
            class="custom-card__image"
          />
          <div class="custom-card__info">
            <div class="custom-card__name">
              {{ item.name }}
            </div>
            <div
              v-show="item.age"
              class="custom-card__age"
            >
              Age: {{ item.age }}
            </div>
          </div>
        </el-button>
        </el-popover>
      </template>
    </VueFamilyTree>
      </el-card>
  </div>
</template>

<script>
import VueFamilyTree from 'vue-family-tree';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    VueFamilyTree,
  },
  props: {
    // eslint-disable-next-line vue/require-prop-type-constructor
    info: {},
  },
  data() {
    return {
      customCard: true,
      userlist: [],
      temptree: [],
      currentchildren: [],
      currentnode: {},
      testnum: 100,
      tree: [{
        firstPerson: {
          name: 'John Walker',
          image: 'https://picsum.photos/300/300?random=1',
          id: 1,
        },
        secondPerson: {
          name: 'Jannet Grem',
          image: 'https://picsum.photos/300/300?random=2',
          age: 23,
          id: 2,
        },
        children: [{
          firstPerson: {
            name: 'Katia',
            id: 3,
          },
          secondPerson: {
            name: 'Oleg',
            id: 4,
          },
          children: [{
            firstPerson: {
              name: 'Gleb',
              id: 5,
            },
            secondPerson: {
              name: 'Viktoriya',
              id: 6,
            },
            children: [{
              firstPerson: {
                name: 'Rim',
              },
              secondPerson: {
                name: 'Natasha',
              },
            },
            {
              firstPerson: {
                name: 'Leonid',
              },
            }, {
              firstPerson: {
                name: 'Leonid',
              },
              children: [{
                firstPerson: {
                  name: 'Rim',
                },
                secondPerson: {
                  name: 'Natasha',
                },
              }],
            }, {
              firstPerson: {
                name: 'Leonid',
              },
            }],
          },
          {
            firstPerson: {
              name: 'Olga',
            },
            secondPerson: {
              name: 'Nikita',
            },
          }],
        },
        {
          firstPerson: {
            name: 'Vitia',
          },
          secondPerson: {
            name: 'Dasha',
          },
        },
        {
          firstPerson: {
            name: 'Antonio Wild',
            image: 'https://picsum.photos/300/300?random=3',
          },
          secondPerson: {
            name: 'Olivia Olson',
          },
          children: [{
            firstPerson: {
              name: 'Kristina Wild',
            },
          },
          {
            firstPerson: {
              name: 'Alexey Wild',
            },
          },
          {
            firstPerson: {
              name: 'Viktor Wild',
              id: 22,
            },
          }],
        }],
      }],
    };
  },
  methods: {
    cardClick(item) {
      console.log(item);
    },
    getUser() { // 获取userlist
      this.loading = true;
      axios.post('/api/query-user', { group_id: this.$props.info.id })
        .then((res) => {
          this.loading = false;
          if (res.data.status) {
            this.$data.userlist = res.data.user_list;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // 添加成员
    addMember(item, type) {
      console.log(item);
      this.test(this.tree, item.id); // 返回选中节点和层的信息
      if (type === 'Sibling') {
        console.log('addSibling');
        // eslint-disable-next-line no-restricted-syntax
        const ele = { firstPerson: { name: '未定义', id: this.testnum, image: 's' } };
        this.testnum += 1;
        this.currentchildren.push(ele);
        console.log(this.tree);
      } else if (type === 'Children') {
        const ele = { firstPerson: { name: '未定义', id: this.testnum, image: 's' } };
        this.testnum += 1;
        if (this.currentnode.children !== undefined) {
          this.currentnode.children.push(ele);
        } else {
          // eslint-disable-next-line no-param-reassign
          this.currentnode.children = [];
          this.currentnode.children.push(ele);
        }
        console.log('addChildren');
      } else if (type === 'Honey') {
        const ele = { name: '未定义', id: this.testnum, image: 's' };
        if (this.currentnode.firstPerson !== undefined && this.currentnode.secondPerson === undefined) { // 说明只有左节点
          this.currentnode.secondPerson = ele;
          this.testnum += 1;
        } else if (this.currentnode.firstPerson === undefined && this.currentnode.secondPerson !== undefined) { // 说明只有右节点
          this.currentnode.firstPerson = ele;
          this.testnum += 1;
        } else { // 说明两个节点都有
          this.$message({
            type: 'warning',
            message: '无法添加配偶',
          });
        }
        console.log('addHoney');
      } else {
        console.log('Error');
      }
    },
    // 递归遍历所有节点，根据id找到对应的children数组和节点
    test(tree, id) {
      let e;
      this.temptree = tree;
      // eslint-disable-next-line guard-for-in,no-restricted-syntax
      for (e of this.temptree) {
        if (e.firstPerson !== undefined && e.firstPerson.id === id) {
          console.log(e.firstPerson);
          this.currentnode = e;// 当前节点，字典类型
          this.currentchildren = this.temptree; // 当前层，数组类型
          console.log(this.currentchildren);
        }
        if (e.secondPerson !== undefined && e.secondPerson.id === id) {
          this.currentnode = e; // 当前节点，字典类型
          console.log(e.secondPerson);
          this.currentchildren = this.temptree; // 当前层，数组类型
          console.log(this.currentchildren);
        }
        if (e.children !== undefined) { // 若它不是叶子结点
          this.test(e.children, id); // 递归至下一个孩子层
        }
      }
    },
  },
  created() {
    this.getUser();
  },
};
</script>
<style lang="scss" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 30px;
}
.text-center {
  text-align: center;
  margin-bottom: 16px;
}
.custom-card {
  display: flex;
  align-items: center;
  width: 110px;
  padding: 5px;
  border: 0.5px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  background-color: #fff;
  cursor: pointer;
  box-shadow: 0 0 3px 1px rgba(#000, 0);
  transition: box-shadow .2s ease;
  &:hover {
    box-shadow: 0 0 3px 1px rgba(#000, .1);
  }
  &__image {
    flex: 0 0 auto;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #dedede;
    background-size: cover;
    background-position: 50%;
  }
  &__info {
    padding-left: 8px;
  }
  &__name {
    font-weight: 300;
  }
  &__age {
    margin-top: 2px;
    font-size: 6px;
  }
}
</style>

<!--<style lang="scss" scoped>-->
<!--#app {-->
<!--  font-family: Avenir, Helvetica, Arial, sans-serif;-->
<!--  -webkit-font-smoothing: antialiased;-->
<!--  -moz-osx-font-smoothing: grayscale;-->
<!--  color: #2c3e50;-->
<!--  margin-top: 60px;-->
<!--}-->
<!--.text-center {-->
<!--  text-align: center;-->
<!--  margin-bottom: 32px;-->
<!--}-->
<!--.custom-card {-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  width: 220px;-->
<!--  padding: 10px;-->
<!--  border: 1px solid #ddd;-->
<!--  border-radius: 10px;-->
<!--  box-sizing: border-box;-->
<!--  background-color: #fff;-->
<!--  cursor: pointer;-->
<!--  box-shadow: 0 0 6px 2px rgba(#000, 0);-->
<!--  transition: box-shadow .2s ease;-->
<!--  &:hover {-->
<!--    box-shadow: 0 0 6px 2px rgba(#000, .1);-->
<!--  }-->
<!--  &__image {-->
<!--    flex: 0 0 auto;-->
<!--    width: 60px;-->
<!--    height: 60px;-->
<!--    border-radius: 50%;-->
<!--    background-color: #dedede;-->
<!--    background-size: cover;-->
<!--    background-position: 50%;-->
<!--  }-->
<!--  &__info {-->
<!--    padding-left: 16px;-->
<!--  }-->
<!--  &__name {-->
<!--    font-weight: 600;-->
<!--  }-->
<!--  &__age {-->
<!--    margin-top: 4px;-->
<!--    font-size: 12px;-->
<!--  }-->
<!--}-->
<!--</style>-->
