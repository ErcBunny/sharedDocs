clear
clc
close all
format rat

A = [0,1,0,0;41.63,0,0,0;0,0,0,1;-0.6099,0,0,0]
B = [0;-2.7584;0;0.6898]
C = [1,0,0,0;0,0,1,0]
D = [0;0]

Q = C'*C;
R = 0.1
Q(1,1)=1000;
Q(3,3)=1000;

[K, P] = lqr(A,B,Q,R)

t = 0:0.01:10;
U_1 = 1*ones(size(t));
U_1(1:200) = 0;
x_init_1 = [0,0,0,0];
[Y1,X1] = lsim(A-B*K,B,C,D,U_1,t,x_init_1);
U_2 = zeros(size(t));
x_init_2 = [0.1,0,0,0];
[Y2,X2] = lsim(A-B*K,B,C,D,U_2,t,x_init_2);
U_3 = normrnd(0,1,size(t));
x_init_3 = [0,0,0,0];
[Y3,X3] = lsim(A-B*K,B,C,D,U_3,t,x_init_3);


subplot(3,1,1)
plot(t, Y1)
legend('¦È','x')
title('step response')
grid on

subplot(3,1,2)
plot(t, Y2)
legend('¦È','x')
title('zero input')
grid on

subplot(3,1,3)
plot(t, Y3)
legend('¦È','x')
title('zero state with normrnd input')
grid on
