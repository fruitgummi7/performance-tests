from locust import HttpUser, TaskSet, task, between

# 3 + 2 = 5; 100% / 5 = 20% - вес одной задачи
class BrowseCatalog(TaskSet):
    @task(3) # 3 * 20% = 60%
    def get_product(self):
        self.client.get("/product/123")

    @task(2) # 2 * 20% = 40%
    def get_category(self):
        self.client.get("/category/456")


# 1, 100%
class BrowseBucket(TaskSet):
    @task
    def get_bucket(self):
        self.client.get("/bucket")

class ShopUser(HttpUser):
    host = "https://api.example.com"
    tasks = [BrowseCatalog, BrowseBucket]
    # BrowseCatalog = 50%
    # - get_product: 0.6 * 0.5 = 0.3 => 30%
    # - get_category: 0.4 * 0.5 = 0.2 => 20%

    # BrowseBucket = 50%
    # - get_bucket: 1 * 0.5 = 0.5 => 50%
    wait_time = between(1, 3)



class ShopUser2(HttpUser):
    host = "https://api.example.com"
    # 3 + 7 = 10; 100% / 10 = 10, 1 = 10%
    tasks = {
        BrowseCatalog: 3, # 30%
        BrowseBucket: 7 # 70%
    }
    # BrowseCatalog
    # - get_product: 0.6 * 0.3 = 0.18 => 18%
    # - get_category: 0.4 * 0.3 = 0.12 => 12%
    # BrowseBucket
    # - get_bucket: 1 * 0.7 = 0.7 => 70%
    wait_time = between(1, 3)