import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.mllib.recommendation.Rating
import org.apache.spark.mllib.recommendation.ALS
object sparkALS {
  def main(args: Array[String]): Unit = {
    val conf=new SparkConf().setAppName("als").setMaster("local")
    val sc=new SparkContext(conf)
    val t1=System.currentTimeMillis()
    val rawData = sc.textFile("e://data/me.txt")
     //提取有用的部分数据
    val rawRatings = rawData.map(_.split(",").take(3))
     //将数据转化为指定格式
    val ratings = rawRatings.map { case Array(user, movie, rating) => Rating(user.toInt, movie.toInt, rating.toDouble) }
     //利用ALS自带的train方法，和ratings数据，训练出一个模型
    val model = ALS.train(ratings, 50, 10, 0.01)
    //利用模型预测用户1对商品2的评分
    val predict=model.predict(1,2)
    //利用模型向用户1推荐1个评分最高的商品
    val topKRecs = model.recommendProducts(1, 1)

    val t2=System.currentTimeMillis()
    println("用户1对商品2的预测评分为:"+predict)
    println("向用户1推荐的商品为："+topKRecs.mkString("\n"))
    println("计算36000条数据时，此算法共耗时："+(t2-t1)+"毫秒")

    sc.stop()
  }
}
