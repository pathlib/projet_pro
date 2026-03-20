from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

x= [1,2,3,4,5]
y=[10,20,30,40,50]

x_train,y_train,x_test,y_test=train_test_split(x,y)

model=LinearRegression()

model.fit(x_train,y_train)

y_test=model.predict(x_test)
print(y_test)
