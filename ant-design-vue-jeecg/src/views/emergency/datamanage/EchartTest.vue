<template>
  <div id="myChart" style="width: 100%; height: 500px">
  </div>
</template>

<script>
  import {getAction, postAction} from "@/api/manage";
  import * as echarts from 'echarts';

  export default {
    name: 'EchartTest',
    data(){

    },
    mounted() {
      this.drawEcharts();
    },
    methods:{
      drawEcharts(){
        let option = {
          tooltip: {
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              selectedMode: 'single',
              radius: [0, '30%'],
              label: {
                position: 'inner',
                fontSize: 14
              },
              labelLine: {
              },
              data: [
                { value: 110, name: 'male' },
                { value: 100, name: 'female', selected: true }
              ]
            },
            {
              name: 'Access From',
              type: 'pie',
              radius: ['45%', '60%'],
              labelLine: {
                length: 30
              },
              label: {
                rich: {
                  a: {
                    color: '#6E7079',
                    lineHeight: 22,
                    align: 'center'
                  },
                  hr: {
                    borderColor: '#8C8D8E',
                    width: '100%',
                    borderWidth: 1,
                    height: 0
                  },
                  b: {
                    color: '#4C5058',
                    fontSize: 14,
                    fontWeight: 'bold',
                    lineHeight: 33
                  },
                  per: {
                    color: '#fff',
                    backgroundColor: '#4C5058',
                    padding: [3, 4],
                    borderRadius: 4
                  }
                }
              },
              data: [
                { value: 1048, name: 'Baidu' },
                { value: 335, name: 'Direct' },
                { value: 310, name: 'Email' },
                { value: 251, name: 'Google' },
                { value: 234, name: 'Union Ads' },
                { value: 147, name: 'Bing' },
                { value: 135, name: 'Video Ads' },
                { value: 102, name: 'Others' }
              ]
            }
          ]
        };
        let myChart = echarts.init(document.getElementById('myChart'))
        myChart.setOption(option);
      }
    }
  }

</script>

<style scoped>

</style>