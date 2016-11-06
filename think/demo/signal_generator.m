num_for_each = 1000;
x = [-5:0.1:5];
fout = fopen('raw_data.txt','w');
for i = 1:num_for_each
	i
	%SIN 0
	A = rand()+1;
	b = rand()*pi;
	c = rand();
	y = A*sin(x+b)+c;
	for j = 1:size(y,2)
		fprintf(fout,'%4.5f\t',y(j));
	end
	fprintf(fout, '%d\n', 0);
	%LINEAR 1
	A = rand()+1;
	b = rand();
	y = A*x+b;
	for j = 1:size(y,2)
		fprintf(fout,'%4.5f\t',y(j));
	end
	fprintf(fout, '%d\n', 1);
	%QUADRATIC 2
	A = rand()+1;
	b = rand();
	c = rand();
	y = A*(x.*x)+b*x+c;
	for j = 1:size(y,2)
		fprintf(fout,'%4.5f\t',y(j));
	end
	fprintf(fout, '%d\n', 2);
end
fclose(fout);