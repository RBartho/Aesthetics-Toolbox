function box_count(filename);

% calculates fractal dimension using box counting
% CC/ZJI
%

b = imread(filename)

threshold = mean(mean(b));

b = double(b)<threshold;

subplot 121
imagesc(-b)
shading flat
colormap gray
axis equal

i = 1;
while size(b,1) > 6
    x(i) = size(b,1);
    y(i) = sum(sum(b));
    c = zeros(size(b)./2);
    for xx = 1:size(c,1)
        for yy = 1:size(c,2)
            c(xx,yy) = b(xx*2,yy*2)+b(xx*2-1,yy*2)+b(xx*2,yy*2-1)+b(xx*2-1,yy*2-1);
        end
    end    
    b = c>0 & c<4;
    i = i+1;
end

params = polyfit(log2(x(2:end)'),log2(y(2:end)'),1)
%params = regress(log(y'),log(x'))
%nlinfit(log(x),log(y),'linear',[1 1]);

D = params(1);
title(D)

subplot 122
plot(log2(x(2:end)),log2(y(2:end)),'bo');
hold on
plot([0 8],[params(2) (params(2)+8*params(1))],'r-')
%plot([0 8],[0 8*params(1)],'r-')
axis([0 8 0 16]);    
hold off   

