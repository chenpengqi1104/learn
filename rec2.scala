
import org.apache.log4j.{Level, Logger}

import org.apache.spark.mllib.recommendation.{ALS, MatrixFactorizationModel, Rating}

import org.apache.spark.rdd._

import org.apache.spark.{SparkContext, SparkConf}

import org.apache.spark.SparkContext._
import scala.io.Source
object rec2 {

  def main(args: Array[String]): Unit = {
    val t1=System.currentTimeMillis()
    Logger.getLogger("org.apache.spark").setLevel(Level.WARN)

    Logger.getLogger("org.apache.eclipse.jetty.server").setLevel(Level.OFF)
    val sparkConf = new SparkConf().setAppName("ALS2").setMaster("local[2]")
    val sc = new SparkContext(sparkConf)

    //读取数据集文件并对其进行结构化处理
    //以时间戳对10进行取余为key键，剩下的为value值进行处理
    val ratings = sc.textFile("e://data/me.txt").map {
      line =>
        val fields = line.split(",")
        (fields(3).toLong % 10, Rating(fields(0).toInt, fields(1).toInt, fields(2).toDouble))
    }


    //统计用户数量和电影数量以及用户对电影的评分数目
    val numRatings = ratings.count()
    val numUsers = ratings.map(_._2.user).distinct().count()
    val numMovies = ratings.map(_._2.product).distinct().count()
    println("一共有： " + numRatings + "个评分，" + numUsers + " 个用户，" + numMovies + "个电影")


    //将样本评分数据集以key值切分成3个部分，分别用于训练(60%，并加入用户评分), 校验 (20%), and 测试 (20%)
    //该数据在计算过程中要多次应用到，所以cache到内存
    val numPartitions = 4

    //训练集
    val training = ratings.filter(x => x._1 < 6).values.repartition(numPartitions).persist()

    //校验集
    val validation = ratings.filter(x => x._1 >= 6 && x._1 < 8).values.repartition(numPartitions).persist()

    //测试集
    val test = ratings.filter(x => x._1 >= 8).values.persist()

    val numTraining = training.count()
    val numValidation = validation.count()
    val numTest = test.count()
    println("训练集的数据量为: " + numTraining + "， 校验集的数据量为: " + numValidation + "， 测试集的数据量为: " + numTest)

    //训练不同参数下的模型，获取最佳参数下的模型
    val ranks = List(8, 12)   //隐含因子数范围
    val lambdas = List(0.1, 10.0)  //正则化系数范围
    val numIters = List(10, 20)   //迭代次数范围
    var bestModel: Option[MatrixFactorizationModel] = None
    var bestValidationRmse = Double.MaxValue
    var bestRank = 0
    var bestLambda = -1.0
    var bestNumIter = -1


    for (rank <- ranks; lambda <- lambdas; numIter <- numIters) {
      //训练出模型
      val model = ALS.train(training, rank, numIter, lambda)

      //将模型放到校验集中进行验证
      val validationRmse = computeRmse(model, validation, numValidation)
      println("校验集中的RMSE值为： " + validationRmse + " ，此时各个参数值为： rank="
        + rank + ",lambda = " + lambda + ",numIter = " + numIter + ".")

      if (validationRmse < bestValidationRmse){
        bestModel = Some(model)
        bestValidationRmse = validationRmse
        bestRank = rank
        bestLambda = lambda
        bestNumIter = numIter
      }
    }
      //用最佳模型预测测试集的评分，并计算和实际评分之间的均方根误差（RMSE）
      val testRmse = computeRmse(bestModel.get, test, numTest)
      println("最佳模型的参数为：rank = " + bestRank + " ，lambda = " + bestLambda
        + ", numIter = " + bestNumIter + ", 测试集的RMSE值为：" + testRmse + ".")

      val meanRating = training.union(validation).map(_.rating).mean
      val baselineRmse = math.sqrt(test.map(x => (meanRating - x.rating) * (meanRating - x.rating)).reduce(_ + _) / numTest)
      val improvement = (baselineRmse - testRmse) / baselineRmse * 100
      println("最佳模型将精度提高了：" + "%1.2f".format(improvement) + "%.")


    //预测用户1对商品2 的评分
    val predict=bestModel.get.predict(1,2)
    val recList=bestModel.get.recommendProducts(1,5)
    val t2=System.currentTimeMillis()
    val data=recList.mkString("\n")
    println("计算此"+numUsers+"个用户数据据共耗时："+(t2-t1)+"毫秒")
    println("用户1对商品2的预测评分为："+predict)

    println("向用户1推荐的商品为："+data)
    sc.stop()
  }

  //根据传入的参数计算均方根误差
  def computeRmse(model:MatrixFactorizationModel,data:RDD[Rating],n:Long):Double = {
    val predictions:RDD[Rating] = model.predict((data.map(x => (x.user,x.product))))
    val predictionsAndRatings = predictions.map{ x =>((x.user,x.product),x.rating)}
      .join(data.map(x => ((x.user,x.product),x.rating))).values
    math.sqrt(predictionsAndRatings.map( x => (x._1 - x._2) * (x._1 - x._2)).reduce(_+_)/n)
  }
}








