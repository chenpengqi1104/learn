import breeze.linalg._
import org.apache.spark.{SparkConf, SparkContext}
import scala.util.control.Breaks._
object rec1{

  //定义一个3行4列的矩阵
  val m1 =DenseMatrix.zeros[Double](36000,3)

  //随机初始化分解后的两个矩阵
  val m2=DenseMatrix.zeros[Double](36000,3)


  val m3=DenseMatrix.zeros[Double](3,3)

  val rows=m1.rows //3
  val cols=m1.cols //4
  val rows2=m2.rows//3
  val cols2=m2.cols//2
  val rows3=m3.rows//2
  val cols3=m3.cols//4

  val predictM = DenseMatrix.zeros[Double](rows,cols)

  def main(args: Array[String]): Unit = {
      val conf=new SparkConf().setAppName("r").setMaster("local")
      val sc=new SparkContext(conf)
    val time1=System.currentTimeMillis()
      for(i<-0 to m1.rows-1){
        for(j<- 0 to m1.cols-1){
          m1(i,j)=scala.util.Random.nextInt(5).toDouble
        }
      }
    for(i<-0 to m2.rows-1){
      for(j<- 0 to m2.cols-1){
        m2(i,j)=scala.util.Random.nextInt(5).toDouble
      }
    }
    for(i<-0 to m3.rows-1){
      for(j<- 0 to m3.cols-1){
        m3(i,j)=scala.util.Random.nextInt(5).toDouble
      }
    }

      val data1=sc.textFile("e://data/me.txt",5)
      val data=data1.map(_.split(",").take(3))



      train()  //调用训练模型方法，得出合适的模型


      val a=predict(1,2)//进行预测算法，预测用户1对商品2 的评分

      val b=Recommend(1,1)//向用户1推荐评分top(2)的商品

      println("用户1对商品2的预测评分为："+a)//进行预测算法，预测用户1对商品2 的评分
      println("向用户1推荐的个商品为："+b)//向用户1推荐评分top(n)的商品
    val time2=System.currentTimeMillis()
    val time=(time2-time1)
    println("训练此"+rows+"条数据的模型耗时："+time+"毫秒")
  }


  def train():Unit= {


    var res = 0.0
    val alpha = 0.0001
    val beta = 0.02
    //控制循环的次数
    for (step <- 0 to 5000) {

      for (i <- 0 to rows-1) {//用户的数量，即m1的行数
        for (j <- 0 to cols-1) { //商品的数量，即m1的列数
          if (m1(i, j) > 0) {
            var error = m1(i, j)  //给误差定义一个初始值

            for (k <- 0 to cols2-1) {
              error = error - m2(i, k) * m3(k, j)
            }
            //更新m2和m3中对应位置的值
            for (k <- 0 to cols2-1) {
              m2(i, k) = m2(i, k) + alpha * (2 * error * m3(k, j) - beta * m2(i, k))
              m3(k, j) = m3(k, j) + alpha * (2 * error * m2(i, k) - beta * m3(k, j))
            }

          }
        }
      }

      var loss = 0.0   // 计算整个矩阵的RMSE值
      for (i <- 0 to rows-1) {
        for (j <- 0 to cols-1) {
          if (m1(i, j) > 0) {
            var error = 0.0
            for (k <- 0 to cols2-1) {
              error = error + m2(i, k) * m3(k, j)
            }
            loss = loss + (m1(i, j) - error) * (m1(i, j) - error)
            for (k <- 0 to cols2-1) {
              loss = loss + (beta / 2) * (m2(i, k) * m2(i, k) + m3(k, j) * m3(k, j))
            }

          }
        }
      }
      if (loss <= 0.01) {
        break()
      }
      if (step % 100 == 0) {
        println("迭代了" + step / 100 + "次后的损失函数值为：" + loss)
        println("m2为：")
        println(m2)
        println("m3为：")
        println(m3)
      }
    }

    println("迭代完的评分预测矩阵为：")
    for (a <- 0 to rows - 1) { //m1的列数从0到3
      for (i <- 0 to cols3 - 1) {

        for (j <- 0 to rows3 - 1) { //算出m1(a,i)的预测值
          res = (res + m2(a, j) * m3(j, i))
        }

        predictM(a,i)=res
      }
    }
   println(predictM)

  }
  def predict( uid:Int,pid:Int):Double={//预测用户i对商品j的评分
    val i=uid-1
    val j=pid-1
    predictM(i,j)
  }

  def Recommend(uid:Int,num:Int):String={ //向用户uid推荐num个评分可能最高的商品,返回一个有序评分数组
    val i=uid-1
    var res=0.0
    var str=""
    var max=0.0
    for (j<-0 to predictM.cols-1){
      if(predictM(i,j)>max){
        max=predictM(i,j)
      }
      var num=j+1
      str="评分最高的是商品"+num+",评分为："+max
    }

   str

  }




}