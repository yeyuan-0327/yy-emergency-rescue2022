<template>
    <a-card >
      <a-row>
        <a-col :span="6">
            <a-cascader
              size="large"
              :options="options"
              :load-data="loadSelectData"
              placeholder="Please select"
              change-on-select
              style="width: 300px"
              @change="onSelectChange"
            />
          <a-card style="min-height: 500px">
            <a-list item-layout="horizontal" :data-source="list_data">
              <a-list-item slot="renderItem" slot-scope="item, index">
                <a-list-item-meta
                  description="Ant Design, a design language for background applications, is refined by Ant UED Team"
                >
                  <a slot="title" href="https://www.antdv.com/">{{ item.title }}</a>
                  <a-avatar
                    slot="avatar"
                    src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                  />
                </a-list-item-meta>
              </a-list-item>
            </a-list>
          </a-card>
        </a-col>
        <a-col :span="18">
          <a-card style="min-height: 600px">
          </a-card>
        </a-col>
      </a-row>
    </a-card>
</template>

<script>


  const list_data = [
    {
      title: 'Ant Design Title 1',
    },
    {
      title: 'Ant Design Title 2',
    },
    {
      title: 'Ant Design Title 3',
    },
    {
      title: 'Ant Design Title 4',
    },
  ];
  export default {
    name: 'TaskManage',
    data(){
      return {
        options: [
          {
            value: 'zhejiang',
            label: 'Zhejiang',
            isLeaf: false,
          },
          {
            value: 'jiangsu',
            label: 'Jiangsu',
            isLeaf: false,
          },
        ],
        list_data
      };
    },
    methods:{
      // 选择框改变
      onSelectChange(value) {
        console.log(value)
      },
      // 动态加载选择框数据
      loadSelectData(selectedOptions) {
        const targetOption = selectedOptions[selectedOptions.length - 1];
        targetOption.loading = true;

        // load options lazily
        setTimeout(() => {
          targetOption.loading = false;
          targetOption.children = [
            {
              label: `${targetOption.label} Dynamic 1`,
              value: 'dynamic1',
            },
            {
              label: `${targetOption.label} Dynamic 2`,
              value: 'dynamic2',
            },
          ];
          this.options = [...this.options];
        }, 1000);
      },
      //
      similarRecommend(record){
        console.log(record)
      },
      //
      ruleRecommend(record){
        console.log(record)
      }
    }
  }
</script>

<style scoped>
</style>