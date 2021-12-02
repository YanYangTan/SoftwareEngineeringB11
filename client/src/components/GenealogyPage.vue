<template>
  <div>
<TreeChart :json="treeData" />
  </div>
</template>

<script>
import TreeChart from 'vue-tree-chart';

export default {
  name: 'GenealogyPage',
  components: {
    TreeChart,
  },
  data() {
    return {
      treeData: {
        name: 'root',
        image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
        children: [
          {
            name: 'children1',
            image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
          },
          {
            name: 'children2',
            image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
            mate: {
              name: 'mate',
              image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
            },
            children: [
              {
                name: 'grandchild',
                image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
              },
              {
                name: 'grandchild2',
                image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
              },
              {
                name: 'grandchild3',
                image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
              },
            ],
          },
          {
            name: 'children3',
            image_url: 'http://p7.itc.cn/images01/20201127/6f9bc0f1cdfa425eaed5f09b9a714fa0.png',
          },
        ],
      },

    };
  },
};
</script>

<style scoped>

</style>
